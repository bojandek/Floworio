# music_fetcher.py

import logging
import os
import subprocess
import requests
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def _get_ffmpeg_cmd(cmd_name: str) -> str:
    """Get ffmpeg or ffprobe command, using config path if available."""
    try:
        from config.settings import FFMPEG_PATH, FFPROBE_PATH
        if cmd_name == "ffmpeg" and FFMPEG_PATH:
            return FFMPEG_PATH
        elif cmd_name == "ffprobe" and FFPROBE_PATH:
            return FFPROBE_PATH
    except ImportError:
        pass

    # Try to auto-detect from imageio_ffmpeg
    try:
        import imageio_ffmpeg
        imgio_ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        return imgio_ffmpeg_path
    except (ImportError, AttributeError):
        pass

    # Fallback to simple command name (expects ffmpeg in PATH)
    return cmd_name


# Freesound API base URL
FREESOUND_API_URL = "https://freesound.org/apiv2"


def fetch_music(config: dict) -> Path:
    """
    Fetch background music for the video.
    
    Args:
        config: Dictionary containing:
            - query (str): Search query for music (e.g., 'upbeat background music')
            - duration (int, optional): Maximum duration in seconds
            - output_path (str, optional): Path to save the music file
    
    Returns:
        Path to the downloaded music file
    """
    
    # Extract parameters from config
    query = config.get('query', 'upbeat background music')
    max_duration = config.get('duration', 30)
    output_path = config.get('output_path', 'audio/background_music.mp3')
    
    # Create output directory if needed
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Try to fetch from Freesound API
        from config.settings import FREESOUND_API_KEY
        
        if FREESOUND_API_KEY and FREESOUND_API_KEY != "YOUR_KEY":
            # Search for sounds
            search_url = f"{FREESOUND_API_URL}/search/text/"
            params = {
                'token': FREESOUND_API_KEY,
                'query': query,
                'filter': f'duration:[1 TO {max_duration}]',
                'fields': 'id,name,previews'
            }
            
            response = requests.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            results = response.json().get('results', [])
            
            if results:
                # Get the first result
                sound_id = results[0]['id']
                preview_url = results[0]['previews']['preview-hq-mp3']
                
                # Download the music
                audio_response = requests.get(preview_url, timeout=60)
                audio_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(audio_response.content)
                
                logger.info(f'Music downloaded: {output_path}')
                return Path(output_path)
        
        # Fallback: try to get music from YouTube or create placeholder
        logger.warning('No Freesound API key or no results found, checking other sources')

        # Try YouTube first for free music
        yt_result = _get_free_music(query, output_path)
        if yt_result:
            return yt_result

        return _create_fallback_music(output_path)

    except Exception as e:
        logger.error(f'Music fetch failed: {str(e)}')
        return _create_fallback_music(output_path)


def _create_fallback_music(output_path: str) -> Path:
    """
    Create a placeholder audio file or use bundled music as fallback.
    Tries ffmpeg first, then falls back to numpy-based silent audio generation.
    """
    import subprocess
    import shutil

    # Check if there's bundled music in assets folder
    assets_music = Path('assets/background_music.mp3')
    if assets_music.exists():
        shutil.copy(assets_music, output_path)
        logger.info(f'Using bundled music: {output_path}')
        return Path(output_path)

    # Try to generate silent audio using ffmpeg first
    try:
        # Use MP3 codec for MP3 output, AAC for M4A/MP4
        codec = 'mp3' if output_path.lower().endswith('.mp3') else 'aac'
        cmd = [
            _get_ffmpeg_cmd('ffmpeg'), '-y', '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100:duration=60',
            '-c:a', codec, '-b:a', '128k', output_path
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f'Generated silent audio: {output_path}')
        return Path(output_path)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.warning(f'FFmpeg failed or not found: {e}')

    # Fallback: generate silent audio using numpy and wave module
    try:
        import numpy as np
        import wave
        import struct

        sample_rate = 44100
        duration = 60  # 60 seconds
        channels = 2
        sampwidth = 2  # 16-bit audio
        nframes = sample_rate * duration
        comp_type = 'NONE'
        comp_name = 'not compressed'

        # Generate silent audio (zeros)
        audio_data = np.zeros((nframes, channels), dtype=np.int16)
        max_sample = 2**(sampwidth * 8 - 1)
        for s in range(nframes):
            for c in range(channels):
                audio_data[s, c] = int(max_sample * 0.3)  # 30% volume

        # Convert to bytes
        out_data = b''.join([struct.pack('<h', sample) for sample in audio_data.flatten()])

        # Write wave file
        with wave.open(output_path.replace('.mp3', '.wav'), 'w') as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sampwidth)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(out_data)

        logger.info(f'Generated silent audio (WAV): {output_path.replace(".mp3", ".wav")}')

        # Try to convert WAV to MP3 using ffmpeg if available, otherwise return WAV
        try:
            cmd = [_get_ffmpeg_cmd('ffmpeg'), '-y', '-i', output_path.replace('.mp3', '.wav'), '-c:a', 'mp3', '-b:a', '128k', output_path]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            # Remove temp WAV file
            Path(output_path.replace('.mp3', '.wav')).unlink(missing_ok=True)
            logger.info(f'Converted to MP3: {output_path}')
            return Path(output_path)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # If ffmpeg not available, return WAV
            logger.warning('ffmpeg not available, using WAV format')
            return Path(output_path.replace('.mp3', '.wav'))

    except Exception as e:
        logger.error(f'Audio generation failed: {e}')
        # Fallback to empty file if everything fails
        Path(output_path).touch()
        logger.warning(f'Created empty placeholder: {output_path}')
        return Path(output_path)


def _get_free_music(query: str, output_path: str) -> Optional[Path]:
    """
    Try to get music from free sources without API key.
    Returns None if no free source is available.
    """
    # Try using YouTube search for royalty-free music
    # This requires yt-dlp to be installed
    try:
        import yt_dlp
    except ImportError:
        return None

    # Get ffmpeg path from imageio_ffmpeg for yt-dlp postprocessing
    ffmpeg_path = None
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    except (ImportError, AttributeError):
        pass

    # YouTube search for royalty-free music
    search_queries = [
        f"{query} royalty free",
        "background music no copyright",
        "calm instrumental music"
    ]

    for search_query in search_queries:
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'direct',
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            # Add ffmpeg location if available
            if ffmpeg_path:
                ydl_opts['ffmpeg_location'] = ffmpeg_path

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Search on YouTube
                search_url = f"ytsearch1:{search_query}"
                result = ydl.extract_info(search_url, download=True)
                if result and 'entries' in result:
                    logger.info(f'Music downloaded from YouTube: {output_path}')
                    # yt-dlp may add .mp3 extension, so check for .mp3.mp3 and rename
                    backup_path = Path(output_path)
                    if backup_path.exists():
                        return backup_path
                    # Check if .mp3.mp3 was created (yt-dlp quirk)
                    double_ext_path = Path(str(output_path) + '.mp3')
                    if double_ext_path.exists():
                        double_ext_path.rename(backup_path)
                        logger.info(f'Renamed {double_ext_path} to {backup_path}')
                        return backup_path
                    return backup_path
        except Exception as e:
            logger.warning(f'YouTube download failed: {e}')
            continue

    return None


# Test function
if __name__ == '__main__':
    test_config = {
        'query': 'upbeat background music',
        'duration': 30,
        'output_path': 'audio/test_music.mp3'
    }
    fetch_music(test_config)