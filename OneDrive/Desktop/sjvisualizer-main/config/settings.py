# config/settings.py

# Google Sheets
SPREADSHEET_ID    = "PASTE_YOUR_SPREADSHEET_ID_HERE"
SHEET_NAME        = "Konfiguracija"
SERVICE_ACCT_FILE = "credentials.json"

# TTS engine: "edge" (free) | "elevenlabs" | "openai"
TTS_ENGINE   = "edge"
TTS_LANGUAGE = "en"   # "en" | "bs" | "hr" | "sr"
TTS_VOICE    = "en-US-AriaNeural"

# ElevenLabs (only if TTS_ENGINE = "elevenlabs")
ELEVENLABS_API_KEY  = "YOUR_KEY"
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

# OpenAI (only if TTS_ENGINE = "openai")
OPENAI_API_KEY = "YOUR_KEY"

# Anthropic (for script generation)
ANTHROPIC_API_KEY = "YOUR_KEY"

# Freesound (background music)
FREESOUND_API_KEY = "YOUR_KEY"

# YouTube
YOUTUBE_CLIENT_SECRETS_FILE = "youtube_client_secrets.json"
YOUTUBE_TOKEN_FILE          = "youtube_token.json"
YOUTUBE_DEFAULT_PLAYLIST_ID = ""         # optional
YOUTUBE_PRIVACY_STATUS      = "public"   # "public" | "unlisted" | "private"

# Pipeline timing
SCHEDULER_TIME      = "06:00"
CACHE_MAX_AGE_DAYS  = 7

# Video settings
ASPECT_RATIO   = "1:1"   # "16:9" | "1:1" | "4:5" | "9:16"
VIDEO_FPS      = 60
VIDEO_DURATION = 0.55
MUSIC_VOLUME   = 0.20