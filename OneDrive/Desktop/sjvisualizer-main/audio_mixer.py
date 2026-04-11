# audio_mixer.py

import logging
import subprocess
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)

def mix_audio(
    video_path: Union[str, Path],
    narration_path: Union[str, Path],
    music_path: Union[str, Path],
    output_path: Union[str, Path]
) -> Path:
    """
    Mix audio streams using ffmpeg.
    
    Args:
        video_path: Path to the video file
        narration_path: Path to the narration audio file
        music_path: Path to the background music file
        output_path: Path for the final output video
    
    Returns:
        Path to the mixed audio video file
    """
    
    video_path = Path(video_path)
    narration_path = Path(narration_path)
    music_path = Path(music_path)
    output_path = Path(output_path)
    
    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Calculate fade start time (3 seconds before end)
    # We'll get video duration using ffprobe
    try:
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        fade_start = max(0, duration - 3)  # Start fade out 3 seconds before end
    except Exception as e:
        logger.warning(f"Could not get video duration, using default fade: {e}")
        # Default to 5 seconds before end for a 0.55 minute video
        fade_start = 30  # 30 seconds for a typical video
    
    # Build ffmpeg command
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-i', str(narration_path),
        '-i', str(music_path),
        '-filter_complex',
        f"[1:a]volume=1.0[n];[2:a]volume=0.20,afade=t=in:d=2,afade=t=out:st={fade_start}:d=3[m];[n][m]amix=inputs=2:duration=first[a]",
        '-map', '0:v',
        '-map', '[a]',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        str(output_path)
    ]
    
    logger.info(f"Running ffmpeg command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f"Audio mixing completed: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg failed: {e.stderr}")
        raise RuntimeError(f"Audio mixing failed: {e.stderr}")

def mix_video_only(
    video_path: Union[str, Path],
    narration_path: Union[str, Path],
    output_path: Union[str, Path]
) -> Path:
    """
    Mix video with narration only (no background music) - for testing.
    
    Args:
        video_path: Path to the video file
        narration_path: Path to the narration audio file
        output_path: Path for the final output video
    
    Returns:
        Path to the mixed audio video file
    """
    
    video_path = Path(video_path)
    narration_path = Path(narration_path)
    output_path = Path(output_path)
    
    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Build ffmpeg command for video + narration only
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-i', str(narration_path),
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        str(output_path)
    ]
    
    logger.info(f"Running ffmpeg command (video only): {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f"Video+narration mixing completed: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg failed: {e.stderr}")
        raise RuntimeError(f"Video+narration mixing failed: {e.stderr}")

# Test function
if __name__ == '__main__':
    # Simple test - would need actual files to run
    print("Audio mixer module ready")