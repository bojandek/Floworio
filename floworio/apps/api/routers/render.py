"""
Render Router — Video rendering using Remotion
Triggers Node.js Remotion renderer and tracks job progress
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import uuid
import json
import subprocess
import asyncio
from typing import Optional, Dict, Any

router = APIRouter()

RENDERS_DIR = "renders"
os.makedirs(RENDERS_DIR, exist_ok=True)

# Job store (use Redis in production)
render_jobs: Dict[str, Dict] = {}


class RenderConfig(BaseModel):
    chartType: str
    aspectRatio: str
    duration: int
    fps: int
    title: str
    subtitle: str
    backgroundColor: str
    fontColor: str
    colors: Dict[str, str]
    numberOfBars: int
    unit: str
    timeIndicator: str


class StoryData(BaseModel):
    script: Optional[str] = None
    voiceId: Optional[str] = None
    audioUrl: Optional[str] = None


class RenderRequest(BaseModel):
    data_id: str
    config: RenderConfig
    story: Optional[StoryData] = None


class RenderStartResponse(BaseModel):
    job_id: str
    status: str
    message: str


class RenderStatusResponse(BaseModel):
    job_id: str
    status: str  # pending, rendering, completed, failed
    progress: int  # 0-100
    message: str
    video_url: Optional[str] = None
    error: Optional[str] = None


def get_dimensions(aspect_ratio: str) -> tuple[int, int]:
    """Get video dimensions from aspect ratio"""
    dimensions = {
        "16:9": (1920, 1080),
        "9:16": (1080, 1920),
        "1:1": (1080, 1080),
        "4:5": (1080, 1350),
    }
    return dimensions.get(aspect_ratio, (1920, 1080))


async def run_remotion_render(job_id: str, data_id: str, config: dict, story: dict, output_path: str):
    """
    Run Remotion render in background
    Calls: npx remotion render <composition> <output> --props=<json>
    """
    render_jobs[job_id]["status"] = "rendering"
    render_jobs[job_id]["progress"] = 5
    render_jobs[job_id]["message"] = "Fetching animation data..."

    try:
        # Import data store
        from routers.upload import data_store

        if data_id not in data_store:
            raise Exception("Data not found")

        stored = data_store[data_id]

        # Get interpolated frames
        import pandas as pd
        import numpy as np
        import datetime

        df = pd.read_json(stored["df_json"])

        # Interpolate
        total_frames = config["fps"] * config["duration"]

        render_jobs[job_id]["progress"] = 15
        render_jobs[job_id]["message"] = "Interpolating data frames..."

        from routers.upload import interpolate_dataframe
        interpolated_df = interpolate_dataframe(df, total_frames)

        # Convert to frames array
        frames_data = []
        for idx, row in interpolated_df.iterrows():
            frames_data.append({
                "timestamp": str(idx),
                "values": {col: float(val) for col, val in row.items()}
            })

        render_jobs[job_id]["progress"] = 30
        render_jobs[job_id]["message"] = "Preparing Remotion composition..."

        # Build Remotion props
        width, height = get_dimensions(config["aspectRatio"])
        remotion_props = {
            "frames": frames_data,
            "config": config,
            "story": story,
            "width": width,
            "height": height,
            "totalFrames": total_frames,
        }

        # Save props to temp file
        props_file = f"/tmp/floworio_props_{job_id}.json"
        with open(props_file, "w") as f:
            json.dump(remotion_props, f)

        render_jobs[job_id]["progress"] = 40
        render_jobs[job_id]["message"] = "Starting Remotion render engine..."

        # Determine composition ID based on chart type
        composition_map = {
            "bar_race": "BarRace",
            "pie_race": "PieRace",
            "line_chart": "LineChart",
            "area_chart": "AreaChart",
            "world_map": "WorldMap",
        }
        composition_id = composition_map.get(config["chartType"], "BarRace")

        # Path to Remotion project
        remotion_dir = os.path.join(os.path.dirname(__file__), "..", "..", "web")

        # Run Remotion render
        cmd = [
            "npx", "remotion", "render",
            composition_id,
            output_path,
            f"--props={props_file}",
            f"--frames=0-{total_frames - 1}",
            f"--fps={config['fps']}",
            "--codec=h264",
            "--log=verbose",
        ]

        render_jobs[job_id]["progress"] = 50
        render_jobs[job_id]["message"] = "Rendering frames..."

        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=remotion_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Monitor progress
        progress = 50
        async for line in process.stdout:
            line_str = line.decode().strip()
            if "%" in line_str:
                try:
                    pct = int(line_str.split("%")[0].split()[-1])
                    progress = 50 + int(pct * 0.45)
                    render_jobs[job_id]["progress"] = min(progress, 95)
                    render_jobs[job_id]["message"] = f"Rendering... {pct}%"
                except Exception:
                    pass

        await process.wait()

        if process.returncode != 0:
            stderr = await process.stderr.read()
            raise Exception(f"Remotion render failed: {stderr.decode()}")

        # Mix audio if voiceover exists
        if story and story.get("audioUrl"):
            render_jobs[job_id]["progress"] = 96
            render_jobs[job_id]["message"] = "Mixing audio..."
            await mix_audio(output_path, story["audioUrl"])

        render_jobs[job_id]["status"] = "completed"
        render_jobs[job_id]["progress"] = 100
        render_jobs[job_id]["message"] = "Render complete!"

        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        video_filename = os.path.basename(output_path)
        render_jobs[job_id]["video_url"] = f"{base_url}/renders/{video_filename}"

    except Exception as e:
        render_jobs[job_id]["status"] = "failed"
        render_jobs[job_id]["error"] = str(e)
        render_jobs[job_id]["message"] = f"Render failed: {str(e)}"
        print(f"Render error for job {job_id}: {e}")


async def mix_audio(video_path: str, audio_url: str):
    """Mix voiceover audio into video using FFmpeg"""
    try:
        import httpx
        # Download audio
        audio_path = video_path.replace(".mp4", "_audio.wav")
        async with httpx.AsyncClient() as client:
            response = await client.get(audio_url)
            with open(audio_path, "wb") as f:
                f.write(response.content)

        # Mix with FFmpeg
        output_with_audio = video_path.replace(".mp4", "_final.mp4")
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_with_audio,
        ]
        process = await asyncio.create_subprocess_exec(*cmd)
        await process.wait()

        if process.returncode == 0:
            os.replace(output_with_audio, video_path)
            os.remove(audio_path)

    except Exception as e:
        print(f"Audio mixing failed: {e}")


@router.post("/start", response_model=RenderStartResponse)
async def start_render(request: RenderRequest, background_tasks: BackgroundTasks):
    """Start a video render job"""
    job_id = str(uuid.uuid4())
    output_filename = f"floworio_{job_id}.mp4"
    output_path = os.path.join(RENDERS_DIR, output_filename)

    render_jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "message": "Queued for rendering...",
        "video_url": None,
        "error": None,
    }

    story_dict = request.story.model_dump() if request.story else {}
    config_dict = request.config.model_dump()

    background_tasks.add_task(
        run_remotion_render,
        job_id=job_id,
        data_id=request.data_id,
        config=config_dict,
        story=story_dict,
        output_path=output_path,
    )

    return RenderStartResponse(
        job_id=job_id,
        status="pending",
        message="Render job queued successfully",
    )


@router.get("/status/{job_id}", response_model=RenderStatusResponse)
async def get_render_status(job_id: str):
    """Get the status of a render job"""
    if job_id not in render_jobs:
        raise HTTPException(status_code=404, detail="Render job not found")

    job = render_jobs[job_id]
    return RenderStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        message=job["message"],
        video_url=job.get("video_url"),
        error=job.get("error"),
    )


@router.get("/jobs")
async def list_render_jobs():
    """List all render jobs"""
    return {
        "jobs": [
            {"job_id": jid, **{k: v for k, v in job.items()}}
            for jid, job in render_jobs.items()
        ]
    }
