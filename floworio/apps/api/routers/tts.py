"""
TTS Router — Text-to-Speech using Kokoro TTS (open-source)
GitHub: https://github.com/hexgrad/kokoro
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import uuid
from typing import Optional

router = APIRouter()

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Available Kokoro voices
KOKORO_VOICES = {
    "af_heart": "Heart (Female, EN)",
    "af_bella": "Bella (Female, EN)",
    "af_nicole": "Nicole (Female, EN)",
    "af_sarah": "Sarah (Female, EN)",
    "am_adam": "Adam (Male, EN)",
    "am_michael": "Michael (Male, EN)",
    "bf_emma": "Emma (Female, EN-GB)",
    "bf_isabella": "Isabella (Female, EN-GB)",
    "bm_george": "George (Male, EN-GB)",
    "bm_lewis": "Lewis (Male, EN-GB)",
}


class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = "af_heart"
    speed: Optional[float] = 1.0


class TTSResponse(BaseModel):
    audio_url: str
    duration: float
    voice_id: str


@router.post("/generate", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """
    Generate voiceover audio using Kokoro TTS
    Falls back to a simple message if Kokoro is not installed
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if len(request.text) > 10000:
        raise HTTPException(status_code=400, detail="Text too long (max 10,000 characters)")

    voice_id = request.voice_id or "af_heart"
    if voice_id not in KOKORO_VOICES:
        voice_id = "af_heart"

    audio_filename = f"{uuid.uuid4()}.wav"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)

    # Try Kokoro TTS
    kokoro_available = False
    try:
        from kokoro import KPipeline
        import soundfile as sf
        import numpy as np

        pipeline = KPipeline(lang_code='a')  # 'a' for American English
        generator = pipeline(
            request.text,
            voice=voice_id,
            speed=request.speed or 1.0,
            split_pattern=r'\n+'
        )

        audio_chunks = []
        for _, _, audio in generator:
            audio_chunks.append(audio)

        if audio_chunks:
            import numpy as np
            full_audio = np.concatenate(audio_chunks)
            sf.write(audio_path, full_audio, 24000)
            duration = len(full_audio) / 24000
            kokoro_available = True

    except ImportError:
        print("Kokoro TTS not installed. Run: pip install kokoro soundfile")
    except Exception as e:
        print(f"Kokoro TTS error: {e}")

    # Fallback: create a silent placeholder audio file
    if not kokoro_available:
        try:
            import wave
            import struct
            import math

            # Create a simple sine wave as placeholder
            sample_rate = 24000
            duration_seconds = len(request.text.split()) / 2.5  # estimate
            num_samples = int(sample_rate * duration_seconds)

            with wave.open(audio_path, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                # Write silence
                wav_file.writeframes(b'\x00\x00' * num_samples)

            duration = duration_seconds
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

    # Return URL to audio file
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    audio_url = f"{base_url}/audio/{audio_filename}"

    return TTSResponse(
        audio_url=audio_url,
        duration=duration,
        voice_id=voice_id,
    )


@router.get("/voices")
async def list_voices():
    """List available TTS voices"""
    return {
        "voices": [
            {"id": voice_id, "name": name}
            for voice_id, name in KOKORO_VOICES.items()
        ],
        "default": "af_heart",
        "engine": "Kokoro TTS (open-source)",
        "github": "https://github.com/hexgrad/kokoro",
    }
