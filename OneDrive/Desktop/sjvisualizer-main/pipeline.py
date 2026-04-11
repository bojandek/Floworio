# pipeline.py

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def run_pipeline(config: Optional[Dict[str, Any]] = None, dry_run: bool = False) -> Optional[Path]:
    """
    Main pipeline orchestrator with optional dry-run mode.

    Args:
        config: Optional configuration dict. If not provided, will fetch from sheets_config.
        dry_run (bool): If True, skips video rendering and upload steps.

    Returns:
        Path to the final rendered video file (or None if dry_run is True and no video is generated)
    """
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info(f"Pipeline started at {start_time}")
    if dry_run:
        logger.warning("Running in DRY-RUN mode. No video rendering or uploads will occur.")
    logger.info("=" * 60)

    try:
        if config is None:
            from sheets_config import get_config_for_today
            config = get_config_for_today()
        logger.info(f"Config loaded: {config.get('title', 'Unknown')}")

        # STEP 2: Render video
        video_path = None
        if not dry_run:
            logger.info("[2/7] Rendering video...")
            from chart_router import render_chart
            video_path = render_chart(config)
            logger.info(f"Video rendered: {video_path}")
        else:
            logger.warning("[2/7] Skipping video rendering in dry-run mode.")
            video_path = Path("output/dry_run_video.mp4")

        # STEP 3: Voiceover
        logger.info("[3/7] Generating voiceover...")
        from voice_generator import generate_voiceover
        voice_config = {
            'text': config.get('subtitle', 'Data visualization'),
            'language': config.get('language', 'en'),
            'voice': config.get('voice', 'en-US-AriaNeural'),
            'output_path': 'audio/narration.mp3'
        }
        narration_path = generate_voiceover(voice_config)
        logger.info(f"Voiceover generated: {narration_path}")

        # STEP 4: Music
        logger.info("[4/7] Fetching background music...")
        from music_fetcher import fetch_music
        music_config = {
            'query': config.get('music_query', 'upbeat background'),
            'duration': 30,
            'output_path': 'audio/background_music.mp3'
        }
        music_path = fetch_music(music_config)
        logger.info(f"Music fetched: {music_path}")

        # STEP 5: Mix
        logger.info("[5/7] Mixing audio with video...")
        from audio_mixer import mix_audio
        title_safe = config.get('title', 'video').replace(' ', '_').replace('/', '_')
        final_output = Path('output') / f"final_{title_safe}.mp4"
        final_path = None
        if not dry_run:
            final_path = mix_audio(
                video_path=video_path,
                narration_path=narration_path,
                music_path=music_path,
                output_path=final_output
            )
            logger.info(f"Final video created: {final_path}")
        else:
            logger.warning("[5/7] Skipping audio mixing in dry-run mode.")
            final_path = Path("output/dry_run_final_video.mp4")

        # STEP 6: Upload (stub)
        if not dry_run:
            logger.info("[6/7] Upload to YouTube (stubbed)...")
            _stub_upload(final_path)
        else:
            logger.warning("[6/7] Skipping upload in dry-run mode.")

        # STEP 7: Notify (stub)
        if not dry_run:
            logger.info("[7/7] Sending notification (stubbed)...")
            _stub_notify(final_path)
        else:
            logger.warning("[7/7] Skipping notification in dry-run mode.")

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info("=" * 60)
        logger.info(f"Pipeline completed {'in dry-run mode' if dry_run else 'successfully'} in {duration:.1f} seconds")
        if not dry_run:
            logger.info(f"Output: {final_path}")
        else:
            logger.info("Dry-run completed. No actual output file was generated.")
        logger.info("=" * 60)

        return final_path
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        raise


def _stub_upload(video_path: Path) -> None:
    """Placeholder for YouTube upload functionality."""
    logger.info(f"[STUB] Would upload {video_path} to YouTube")
    # TODO: Implement YouTube upload using google-api-python-client
    pass


def _stub_notify(video_path: Path) -> None:
    """Placeholder for notification functionality."""
    logger.info(f"[STUB] Would send notification for {video_path}")
    # TODO: Implement notification (email, Discord webhook, etc.)
    pass


if __name__ == '__main__':
    test_config = {
        'title': 'Test Video',
        'subtitle': 'This is a test video',
        'chart_type': 'bar_race',
        'excel_file': 'sjvisualizer-main/sjvisualizer-main/Examples/Data/FAOSTAT.xlsx',
        'aspect_ratio': '1:1',
        'fps': 60,
        'duration': 0.55,
        'record': True
    }
    run_pipeline(test_config, dry_run=True)
