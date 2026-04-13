# audio_mixer.py

import logging
import subprocess
import shutil
import os
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def _get_ffmpeg_cmd(cmd_name: str) -> str:
    """Get ffmpeg or ffprobe command, using config path if available."""
    from config.settings import FFMPEG_PATH, FFPROBE_PATH

    # First check if config has a path
    if cmd_name == "ffmpeg" and FFMPEG_PATH:
        return FFMPEG_PATH
    elif cmd_name == "ffprobe" and FFPROBE_PATH:
        return FFPROBE_PATH

    # Try to auto-detect from imageio_ffmpeg (installed via moviepy)
    try:
        import imageio_ffmpeg
        # imageio_ffmpeg provides get_ffmpeg_exe() which returns the full path
        imgio_ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        if cmd_name == "ffmpeg":
            return imgio_ffmpeg_path
        elif cmd_name == "ffprobe":
            # imageio_ffmpeg doesn't provide ffprobe, so we try to find it
            # or use ffmpeg with same directory
            import os
            ffmpeg_dir = os.path.dirname(imgio_ffmpeg_path)
            ffprobe_path = os.path.join(ffmpeg_dir, 'ffprobe.exe')
            if os.path.exists(ffprobe_path):
                return ffprobe_path
            # Fall back to ffmpeg for duration (slower but works)
            return imgio_ffmpeg_path
    except (ImportError, AttributeError):
        pass

    # Fallback to simple command name (expects ffmpeg in PATH)
    return cmd_name


def get_video_duration(video_path: Path) -> float:
    """Get video duration using various methods with fallbacks."""
    # Method 1: Try ffprobe from ffmpeg
    try:
        probe_cmd = _get_ffmpeg_cmd('ffprobe')
        cmd = [
            probe_cmd, '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        logger.info(f"Video duration: {duration:.2f} seconds")
        return duration
    except Exception as e:
        logger.debug(f"ffprobe failed: {e}")

    # Method 2: Try ffmpeg with null output
    try:
        ffmpeg_cmd = _get_ffmpeg_cmd('ffmpeg')
        cmd = [
            ffmpeg_cmd, '-i', str(video_path), '-t', '0', '-f', 'null', '-'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        # Parse duration from stderr
        for line in result.stderr.split('\n'):
            if 'time=' in line:
                time_str = line.split('time=')[1].split()[0]
                h, m, s = time_str.split(':')
                duration = int(h) * 3600 + int(m) * 60 + float(s)
                logger.info(f"Video duration (from ffmpeg): {duration:.2f} seconds")
                return duration
    except Exception as e:
        logger.debug(f"ffmpeg duration failed: {e}")

    # Method 3: Try moviepy (if installed)
    try:
        from moviepy import VideoFileClip
        clip = VideoFileClip(str(video_path))
        duration = clip.duration
        clip.close()
        logger.info(f"Video duration (from moviepy): {duration:.2f} seconds")
        return duration
    except Exception as e:
        logger.debug(f"moviepy duration failed: {e}")

    # Fallback: assume 5 seconds if duration can't be determined
    logger.warning(f"Could not get video duration, using default 5 seconds")
    return 5.0


def mix_audio(
    video_path: Union[str, Path],
    narration_path: Union[str, Path],
    music_path: Union[str, Path],
    output_path: Union[str, Path]
) -> Path:
    """
    Mix audio streams using ffmpeg with pydub fallback.

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

    # Try ffmpeg first
    try:
        return _mix_audio_ffmpeg(video_path, narration_path, music_path, output_path)
    except (FileNotFoundError, RuntimeError) as e:
        logger.warning(f"FFmpeg failed: {e}, trying pydub fallback...")
        return _mix_audio_pydub(video_path, narration_path, music_path, output_path)


def _mix_audio_ffmpeg(
    video_path: Path,
    narration_path: Path,
    music_path: Path,
    output_path: Path
) -> Path:
    """Mix audio using ffmpeg."""
    # Calculate fade start time (3 seconds before end)
    duration = get_video_duration(video_path)
    fade_start = max(0, duration - 3)  # Start fade out 3 seconds before end

    # Build ffmpeg command
    cmd = [
        _get_ffmpeg_cmd('ffmpeg'), '-y',
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

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    logger.info(f"Audio mixing completed: {output_path}")
    return output_path


def _mix_audio_pydub(
    video_path: Path,
    narration_path: Path,
    music_path: Path,
    output_path: Path
) -> Path:
    """Mix audio using pydub as fallback when ffmpeg is unavailable."""
    try:
        from pydub import AudioSegment
        from pydub.utils import make_chunks
        import tempfile
        import os
    except ImportError:
        raise RuntimeError("pydub is not installed")

    # Get video duration
    duration = get_video_duration(video_path)

    # Load audio files
    try:
        narration = AudioSegment.from_file(str(narration_path))
    except Exception:
        narration = AudioSegment.silent(duration=int(duration * 1000), frame_rate=44100)

    try:
        music = AudioSegment.from_file(str(music_path))
    except Exception:
        music = AudioSegment.silent(duration=int(duration * 1000), frame_rate=44100)

    # Adjust music to match video duration
    if len(music) < len(narration):
        music = music * (len(narration) // len(music) + 1)
    music = music[:len(narration)]

    # Apply volume to music
    music = music - 10  # Reduce music volume by 10dB (approx 0.20 in linear scale)

    # Apply fade in/out to music
    fade_duration = 2000  # 2 seconds
    music = music.fade_in(fade_duration).fade_out(fade_duration)

    # Mix audio
    mixed = narration.overlay(music)

    # Export to output file (MP4 with audio only if no video muxing available)
    # Since ffmpeg isn't available, we'll export as MP3 or WAV
    # First try MP3
    try:
        # Export as MP3 (requires ffmpeg for conversion)
        mixed.export(str(output_path), format='mp3', bitrate='192k')
        logger.info(f"Audio mixing completed (pydub): {output_path}")
        return output_path
    except Exception as e1:
        logger.warning(f"MP3 export failed: {e1}")
        # Try WAV as fallback
        wav_path = output_path.with_suffix('.wav')
        try:
            mixed.export(str(wav_path), format='wav')
            logger.info(f"Audio mixing completed (pydub WAV): {wav_path}")
            return wav_path
        except Exception as e2:
            raise RuntimeError(f"Audio mixing failed: {e1}, {e2}")