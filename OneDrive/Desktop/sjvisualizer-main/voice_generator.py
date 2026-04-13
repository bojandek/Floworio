# voice_generator.py
"""
Generate a voiceover audio file from text using TTS.
"""

import asyncio
import logging
from pathlib import Path
from edge_tts import Communicate
from typing import Dict, Optional

logger = logging.getLogger(__name__)


async def generate_voiceover_async(config: dict) -> Path:
    """
    Generate a voiceover audio file from text using TTS.

    Args:
        config: Dictionary containing:
            - text (str): Text to convert to speech
            - voice (str): Voice identifier (e.g., 'en-US-AriaNeural')
            - output_path (str, optional): Path to save audio file

    Returns:
        Path to the generated audio file
    """
    text = config.get('text', 'Default voiceover text')
    voice = config.get('voice', 'en-US-AriaNeural')
    output_path = config.get('output_path', 'audio/voiceover.mp3')

    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    communicate = Communicate(text, voice=voice)
    await communicate.save(output_path)
    logger.info(f'Voiceover generated: {output_path}')
    return Path(output_path)


def generate_voiceover(config: dict) -> Path:
    """Synchronous wrapper for generate_voiceover_async."""
    return asyncio.run(generate_voiceover_async(config))


if __name__ == '__main__':
    test_config = {
        'text': 'This is a test voiceover for the data visualization pipeline.',
        'voice': 'en-US-AriaNeural',
        'output_path': 'audio/test_voiceover.mp3'
    }
    generate_voiceover(test_config)
