# music_fetcher.py

import logging
import os
import requests
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

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
        
        # Fallback: create a placeholder or use bundled music
        logger.warning('No Freesound API key or no results found, using fallback')
        return _create_fallback_music(output_path)
        
    except Exception as e:
        logger.error(f'Music fetch failed: {str(e)}')
        return _create_fallback_music(output_path)


def _create_fallback_music(output_path: str) -> Path:
    """
    Create a placeholder audio file or use bundled music as fallback.
    """
    # Check if there's bundled music in assets folder
    assets_music = Path('assets/background_music.mp3')
    if assets_music.exists():
        import shutil
        shutil.copy(assets_music, output_path)
        logger.info(f'Using bundled music: {output_path}')
        return Path(output_path)
    
    # Create an empty file as last resort (ffmpeg can handle silence)
    Path(output_path).touch()
    logger.warning(f'Created empty placeholder: {output_path}')
    return Path(output_path)


# Test function
if __name__ == '__main__':
    test_config = {
        'query': 'upbeat background music',
        'duration': 30,
        'output_path': 'audio/test_music.mp3'
    }
    fetch_music(test_config)