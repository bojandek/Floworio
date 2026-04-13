# sheets_config.py

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

import gspread
from oauth2client.service_account import ServiceAccountCredentials

logger = logging.getLogger(__name__)


def get_google_sheet():
    """
    Connect to Google Sheets and return the worksheet.
    Returns None if authentication fails.
    """
    try:
        from config.settings import (
            SPREADSHEET_ID,
            SHEET_NAME,
            SERVICE_ACCT_FILE
        )

        if SPREADSHEET_ID == "PASTE_YOUR_SPREADSHEET_ID_HERE":
            logger.error("SPREADSHEET_ID not configured in config/settings.py")
            return None

        credentials_path = Path(SERVICE_ACCT_FILE)
        if not credentials_path.exists():
            logger.error(f"Service account file not found: {SERVICE_ACCT_FILE}")
            return None

        # Define the scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        # Authenticate using service account
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            str(credentials_path), scope
        )

        # Authorize and open spreadsheet
        gc = gspread.authorize(credentials)
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.worksheet(SHEET_NAME)

        logger.info(f"Connected to Google Sheet: {SHEET_NAME}")
        return worksheet

    except Exception as e:
        logger.error(f"Failed to connect to Google Sheets: {e}")
        return None


def get_config_for_today() -> Optional[Dict[str, Any]]:
    """
    Fetch configuration for today's date from Google Sheets.

    Expected sheet format:
    - Column A: Datum (date in YYYY-MM-DD format)
    - Column B: Naslov (video title)
    - Column C: Subtitle (video subtitle)
    - Column D: Excel fajl (data file path)
    - Column E: Izvor (data source URL)
    - Column F: Chart tip (bar_race, bar, pie, line, map)
    - Column G: Muzika (music query)
    - Column H: Aktivno (TRUE/FALSE)

    Returns:
        Config dict with all settings, or None if not found or error
    """
    worksheet = get_google_sheet()

    if not worksheet:
        logger.warning("Could not connect to Google Sheets")
        return None

    try:
        # Get all records from sheet
        records = worksheet.get_all_records()

        if not records:
            logger.warning("Sheet is empty")
            return None

        today = datetime.now().date()
        today_str = today.strftime("%Y-%m-%d")

        logger.info(f"Looking for config for today: {today_str}")

        # Find config for today
        for record in records:
            # Check if this row is active
            aktivno = str(record.get("Aktivno", "")).strip().lower()
            if aktivno in ["false", "no", "0", ""]:
                continue

            # Check date
            datum = record.get("Datum", "")
            if isinstance(datum, str):
                # Try parsing date string
                try:
                    # Handle common date formats
                    for fmt in ["%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y"]:
                        try:
                            record_date = datetime.strptime(datum, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        logger.warning(f"Could not parse date: {datum}")
                        continue
                except Exception:
                    continue
            elif isinstance(datum, datetime):
                record_date = datum.date()
            else:
                continue

            if record_date == today:
                logger.info(f"Found config for today from row")
                return {
                    'title': record.get("Naslov", "Video"),
                    'subtitle': record.get("Subtitle", "Data visualization"),
                    'excel_file': record.get("Excel fajl", "Examples/Data/FAOSTAT.xlsx"),
                    'source_url': record.get("Izvor", ""),
                    'chart_type': record.get("Chart tip", "bar_race"),
                    'music_query': record.get("Muzika", "upbeat background"),
                    'active': True,
                    'language': 'en',
                    'voice': 'en-US-AriaNeural',
                    'aspect_ratio': '1:1',
                    'fps': 60,
                    'duration': 0.55,
                    'record': True
                }

        logger.warning(f"No active configuration found for today ({today_str})")
        return None

    except Exception as e:
        logger.error(f"Error reading Google Sheet: {e}")
        return None


def get_all_configs() -> list:
    """
    Get all configurations from the sheet without filtering by date.

    Returns:
        List of config dicts
    """
    worksheet = get_google_sheet()

    if not worksheet:
        return []

    try:
        records = worksheet.get_all_records()
        configs = []

        for record in records:
            if str(record.get("Aktivno", "")).strip().lower() not in ["false", "no", "0", ""]:
                configs.append({
                    'title': record.get("Naslov", "Video"),
                    'subtitle': record.get("Subtitle", ""),
                    'excel_file': record.get("Excel fajl", ""),
                    'source_url': record.get("Izvor", ""),
                    'chart_type': record.get("Chart tip", "bar_race"),
                    'music_query': record.get("Muzika", ""),
                    'active': True
                })

        return configs
    except Exception as e:
        logger.error(f"Error reading configs: {e}")
        return []


def log_to_sheet(log_message: str) -> bool:
    """
    Append a log message to the sheet.

    Args:
        log_message: Message to append

    Returns:
        True if successful, False otherwise
    """
    worksheet = get_google_sheet()

    if not worksheet:
        return False

    try:
        # Append row with timestamp and message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([timestamp, log_message])
        logger.info(f"Logged to sheet: {log_message}")
        return True
    except Exception as e:
        logger.error(f"Failed to log to sheet: {e}")
        return False


# Hardcoded fallback (used if Google Sheets credentials are missing)
FALLBACK_CONFIG = {
    'title': "Tomatoes Production",
    'subtitle': "Historical tomato production trends",
    'chart_type': "bar_race",
    'excel_file': "Examples/Data/FAOSTAT.xlsx",
    'music_query': "upbeat background",
    'active': True,
    'language': 'en',
    'voice': 'en-US-AriaNeural',
    'aspect_ratio': '1:1',
    'fps': 60,
    'duration': 0.55,
    'record': True
}
