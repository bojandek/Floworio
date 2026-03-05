"""
Floworio — Celery Render Worker
Handles async video rendering jobs using Redis as broker
Run with: celery -A workers.render_worker worker --loglevel=info

Install: pip install celery redis
"""

import os
import json
import asyncio
import subprocess
from typing import Optional

# Try to import Celery (optional dependency)
try:
    from celery import Celery
    from celery.utils.log import get_task_logger

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    app = Celery(
        "floworio",
        broker=REDIS_URL,
        backend=REDIS_URL,
    )

    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_acks_late=True,
        worker_prefetch_multiplier=1,  # One task at a time (render is heavy)
        task_time_limit=3600,  # 1 hour max per render
        task_soft_time_limit=3000,  # Soft limit: 50 min
    )

    logger = get_task_logger(__name__)
    CELERY_AVAILABLE = True

except ImportError:
    CELERY_AVAILABLE = False
    print("Celery not installed. Run: pip install celery redis")
    print("Using in-process background tasks instead (not suitable for production)")


# ============================================================
# RENDER TASK
# ============================================================

if CELERY_AVAILABLE:
    @app.task(bind=True, name="render_video")
    def render_video_task(
        self,
        job_id: str,
        data_id: str,
        config: dict,
        story: dict,
        output_path: str,
    ):
        """
        Celery task for rendering a video with Remotion
        Updates task state for progress tracking
        """
        try:
            self.update_state(state="PROGRESS", meta={"progress": 5, "message": "Starting render..."})

            # Import here to avoid circular imports
            import sys
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from routers.upload import data_store, interpolate_dataframe
            import pandas as pd

            if data_id not in data_store:
                raise Exception(f"Data not found: {data_id}")

            stored = data_store[data_id]
            df = pd.read_json(stored["df_json"])

            self.update_state(state="PROGRESS", meta={"progress": 15, "message": "Interpolating data..."})

            total_frames = config["fps"] * config["duration"]
            interpolated_df = interpolate_dataframe(df, total_frames)

            frames_data = []
            for idx, row in interpolated_df.iterrows():
                frames_data.append({
                    "timestamp": str(idx),
                    "values": {col: float(val) for col, val in row.items()}
                })

            self.update_state(state="PROGRESS", meta={"progress": 30, "message": "Preparing Remotion..."})

            # Dimensions
            dimensions = {
                "16:9": (1920, 1080),
                "9:16": (1080, 1920),
                "1:1": (1080, 1080),
                "4:5": (1080, 1350),
            }
            width, height = dimensions.get(config["aspectRatio"], (1920, 1080))

            remotion_props = {
                "frames": frames_data,
                "config": config,
                "story": story,
                "width": width,
                "height": height,
                "totalFrames": total_frames,
            }

            # Write props to temp file
            props_file = f"/tmp/floworio_props_{job_id}.json"
            with open(props_file, "w") as f:
                json.dump(remotion_props, f)

            self.update_state(state="PROGRESS", meta={"progress": 40, "message": "Running Remotion render..."})

            composition_map = {
                "bar_race": "BarRace",
                "pie_race": "PieRace",
                "line_chart": "LineChart",
                "area_chart": "AreaChart",
                "world_map": "WorldMap",
            }
            composition_id = composition_map.get(config["chartType"], "BarRace")

            remotion_dir = os.path.join(os.path.dirname(__file__), "..", "..", "web")

            cmd = [
                "npx", "remotion", "render",
                composition_id,
                output_path,
                f"--props={props_file}",
                f"--frames=0-{total_frames - 1}",
                f"--fps={config['fps']}",
                "--codec=h264",
            ]

            process = subprocess.Popen(
                cmd,
                cwd=remotion_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Monitor progress
            for line in process.stdout:
                if "%" in line:
                    try:
                        pct = int(line.split("%")[0].split()[-1])
                        progress = 40 + int(pct * 0.5)
                        self.update_state(
                            state="PROGRESS",
                            meta={"progress": min(progress, 90), "message": f"Rendering... {pct}%"}
                        )
                    except Exception:
                        pass

            process.wait()

            if process.returncode != 0:
                stderr = process.stderr.read()
                raise Exception(f"Remotion failed: {stderr}")

            # Mix audio if voiceover exists
            if story and story.get("audioUrl"):
                self.update_state(state="PROGRESS", meta={"progress": 95, "message": "Mixing audio..."})
                mix_audio_sync(output_path, story["audioUrl"])

            base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
            video_filename = os.path.basename(output_path)
            video_url = f"{base_url}/renders/{video_filename}"

            return {
                "status": "completed",
                "progress": 100,
                "message": "Render complete!",
                "video_url": video_url,
            }

        except Exception as e:
            logger.error(f"Render task failed: {e}")
            raise


def mix_audio_sync(video_path: str, audio_url: str):
    """Synchronous audio mixing with FFmpeg"""
    try:
        import urllib.request
        audio_path = video_path.replace(".mp4", "_audio.wav")
        urllib.request.urlretrieve(audio_url, audio_path)

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
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            os.replace(output_with_audio, video_path)
            os.remove(audio_path)
    except Exception as e:
        print(f"Audio mixing failed: {e}")


# ============================================================
# CELERY STATUS HELPER
# ============================================================

def get_task_status(task_id: str) -> dict:
    """Get Celery task status — used by render router"""
    if not CELERY_AVAILABLE:
        return {"status": "unknown", "progress": 0, "message": "Celery not available"}

    result = app.AsyncResult(task_id)

    if result.state == "PENDING":
        return {"status": "pending", "progress": 0, "message": "Queued..."}
    elif result.state == "PROGRESS":
        info = result.info or {}
        return {
            "status": "rendering",
            "progress": info.get("progress", 0),
            "message": info.get("message", "Rendering..."),
        }
    elif result.state == "SUCCESS":
        return {
            "status": "completed",
            "progress": 100,
            "message": "Done!",
            "video_url": result.result.get("video_url"),
        }
    elif result.state == "FAILURE":
        return {
            "status": "failed",
            "progress": 0,
            "message": str(result.info),
            "error": str(result.info),
        }
    else:
        return {"status": result.state.lower(), "progress": 0, "message": ""}
