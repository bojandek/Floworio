# scheduler.py

import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import schedule

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def daily_job():
    """Execute the pipeline once per day."""
    logger.info("=" * 60)
    logger.info("Starting scheduled pipeline run")
    logger.info("=" * 60)
    
    try:
        from pipeline import run_pipeline
        output_path = run_pipeline()
        logger.info(f"Scheduled run completed successfully: {output_path}")
    except Exception as e:
        logger.error(f"Scheduled run failed: {str(e)}", exc_info=True)


def main():
    """Run the scheduler."""
    # Load settings to get the scheduled time
    try:
        from config.settings import SCHEDULER_TIME
        schedule_time = SCHEDULER_TIME
    except ImportError:
        schedule_time = "06:00"  # Default
    
    logger.info(f"Scheduler configured to run daily at {schedule_time}")
    
    # Schedule the daily job
    schedule.every().day.at(schedule_time).do(daily_job)
    
    # Also run once on startup (for testing)
    logger.info("Running pipeline once on startup...")
    daily_job()
    
    logger.info("Scheduler started. Press Ctrl+C to exit.")
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        sys.exit(0)


if __name__ == '__main__':
    main()