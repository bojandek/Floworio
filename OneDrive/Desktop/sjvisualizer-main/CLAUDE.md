# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains two related projects:

1. **sjvisualizer** - A Python library for creating data visualizations and animations (bar races, pie races, line charts, area charts) from time-series data in Excel files.

2. **Automation Pipeline** - A complete workflow for automatically generating videos from data:
   - Loads configuration from Google Sheets
   - Renders bar race animations
   - Generates voiceovers using edge-tts
   - Fetches background music from Freesound
   - Mixes audio with video using FFmpeg
   - Schedules daily execution

## Installation

```bash
pip install -r requirements.txt
```

**System dependencies:**
- `ffmpeg` - Required for video/audio processing. Install via:
  - Windows: https://ffmpeg.org/download.html (add to PATH)
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

## Common Development Tasks

### Running the Pipeline

```bash
# Dry-run mode (no video rendering - for testing)
python pipeline.py

# Full pipeline (with rendering)
python pipeline.py
```

### Running Examples

```bash
cd sjvisualizer-main/sjvisualizer-main/Examples/
python basic_bar_race.py
```

### Debugging

- Logs are written to `logs/pipeline_YYYYMMDD.log`
- Check for errors: `grep -r "ERROR" logs/`

## Code Architecture

### Automation Pipeline Modules

| File | Purpose |
|------|---------|
| `pipeline.py` | Main orchestrator with dry-run support |
| `chart_router.py` | Dynamic renderer loader |
| `renderers/bar_race_renderer.py` | Bar race video generation |
| `voice_generator.py` | TTS voiceover generation |
| `music_fetcher.py` | Background music fetching |
| `audio_mixer.py` | FFmpeg audio/video mixing |
| `scheduler.py` | Daily pipeline scheduling |
| `config/settings.py` | All configurable values |
| `sheets_config.py` | Google Sheets config loader |

### Folder Structure

```
├── config/         # Configuration files
├── renderers/      # Video renderers (bar_race, bar, pie, line, map)
├── audio/          # Generated audio files
├── output/         # Final video files
├── logs/           # Pipeline execution logs
├── assets/         # Static assets (logos, icons)
├── sjvisualizer/   # Core library modules
└── Examples/       # Example scripts
```

## Dependencies

**Python packages:**
- `pandas`
- `screeninfo`
- `Pillow`
- `openpyxl`
- `opencv-python`
- `edge-tts`
- `schedule`

## Google Sheets Schema

The pipeline reads configuration from Google Sheets:

| Column | Description |
|--------|-------------|
| A: Datum | Date (YYYY-MM-DD) |
| B: Naslov | Video title |
| C: Subtitle | Video subtitle |
| D: Excel fajl | Data file path |
| E: Izvor | Data source URL |
| F: Chart tip | bar_race, bar, pie, line, map |
| G: Muzika | Music query |
| H: Aktivno | TRUE/FALSE |

## Adding New Chart Types

1. Create `renderers/new_chart_renderer.py` with a `render(config: dict) -> Path` function
2. Add entry to `RENDERER_MAP` in `chart_router.py`
3. Test with `python pipeline.py`

## Dry Run Mode

To test the pipeline without rendering videos:

```python
from pipeline import run_pipeline
config = {...}
run_pipeline(config, dry_run=True)  # Skips rendering, mixing, upload
```

## Troubleshooting

**FFmpeg not found:**
- Ensure FFmpeg is installed and in PATH
- Test: `ffmpeg -version`

**Audio generation fails:**
- Upgrade edge-tts: `pip install edge-tts --upgrade`
- Check voice identifier format: `en-US-AriaNeural`

**Google Sheets connection fails:**
- Verify `SERVICE_ACCT_FILE` path in `config/settings.py`
- Check service account permissions

## CI/CD

GitHub Actions workflow (`.github/workflows/pipeline_test.yml`):
- Linting with black, flake8
- Dry-run test on every push
- Unit tests

## License

MIT