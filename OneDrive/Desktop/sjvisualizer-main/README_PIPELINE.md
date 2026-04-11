# sjvisualizer Pipeline 🎥

Automatizovani pipeline za generisanje video animacija iz Excel podataka sa govornim komentarima, pozadinskom muzikom i objavljivanjem na YouTube.

## Brzi početak

```bash
# Instalacija zavisnosti
pip install -r requirements.txt

# Instalacija FFmpeg (Windows)
# Preuzmi sa: https://ffmpeg.org/download.html
# Dodaj u PATH

# Testiranje (dry-run - bez generisanja videa)
python pipeline.py

# Potvrda da voiceover funkcioniše
python voice_generator.py
```

## Struktura

```
.
├── config/
│   └── settings.py       # Konfiguracija (API keys, TTS, video settings)
├── renderers/
│   ├── bar_race_renderer.py  # Bar race video generator
│   ├── bar_renderer.py       # Stub za bar chart
│   ├── pie_renderer.py       # Stub za pie chart
│   ├── line_renderer.py      # Stub za line chart
│   └── map_renderer.py       # Stub za map chart
├── audio/                  # Generisani audio fajlovi
├── output/                 # Konačni video fajlovi
├── logs/                   # Pipeline logovi
├── assets/                 # Logo i ikonice
├── pipeline.py             # Glavni orchestrator
├── chart_router.py         # Dinamički loader renderera
├── voice_generator.py      # TTS generisanje
├── music_fetcher.py        # Preuzimanje muzike
├── audio_mixer.py          # FFmpeg mixovanje
└── scheduler.py            # Dnevni scheduler
```

## Google Sheets konfiguracija

U Google Sheets tabeli (format u `config/settings.py`):

| Datum | Naslov | Subtitle | Excel fajl | Izvor | Chart tip | Muzika | Aktivno |
|-------|--------|----------|------------|-------|-----------|--------|---------|
| 2026-04-12 | Test Video | Data vizualizacija | data.xlsx | source | bar_race | upbeat | TRUE |

## Kako dodati novi tip charta

1. Kreiraj `renderers/new_chart_renderer.py`:

```python
from pathlib import Path

def render(config: dict) -> Path:
    # Tvoja logika za novi chart tip
    return Path("output/video.mp4")
```

2. Dodaj u `chart_router.py`:

```python
RENDERER_MAP = {
    "bar_race": "renderers.bar_race_renderer",
    "new_chart": "renderers.new_chart_renderer",  # <- dodaj ovo
    # ...
}
```

## Dry-run režim (za testiranje)

Bez generisanja videa:

```bash
# Kroz pipeline.py (podrazumevano dry_run=True u __main__)
python pipeline.py
```

Ili direktno u Python kodu:

```python
from pipeline import run_pipeline

config = {
    'title': 'Test',
    'subtitle': 'Test subtitle',
    'chart_type': 'bar_race',
    'excel_file': 'sjvisualizer-main/sjvisualizer-main/Examples/Data/FAOSTAT.xlsx',
    'aspect_ratio': '1:1'
}

run_pipeline(config, dry_run=True)  # Skips render, mix, upload
```

## Docker (opcionalno)

```dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y ffmpeg
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "pipeline.py"]
```

## Troubleshooting

**FFmpeg not found:**
```bash
# Windows: Dodaj FFmpeg u PATH
# Linux: sudo apt install ffmpeg
# Mac: brew install ffmpeg
```

**Audio issue (edge-tts):**
```bash
pip install edge-tts --upgrade
```

## CI/CD

GitHub Actions se pokreće na svaki push u `main`:
- Linting (black, flake8)
- Dry-run test
- Unit testovi

## Licence

MIT