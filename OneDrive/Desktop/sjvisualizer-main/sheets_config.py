# sheets_config.py

import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import date

def get_config_for_today():
    # Try to fetch from Google Sheets
    try:
        from config.settings import SPREADSHEET_ID, SHEET_NAME, SERVICE_ACCT_FILE
        if not SPREADSHEET_ID or SPREADSHEET_ID == "PASTE_YOUR_SPREADSHEET_ID_HERE":
            raise ValueError("SPREADSHEET_ID not configured")
        
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCT_FILE)
        service = build('sheets', 'v4', credentials=credentials)
        
        # Get today's date in YYYY-MM-DD format
        today = date.today().strftime("%Y-%m-%d")
        
        # Fetch data from the sheet
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:H"
        ).execute()
        
        values = result.get('values', [])  # List of rows
        
        # Find today's row
        for row in values:
            if row and row[0] == today:  # First column is 'Datum'
                return {
                    "Datum": row[0],
                    "Naslov": row[1],
                    "Subtitle": row[2],
                    "Excel fajl": row[3],
                    "Izvor": row[4],
                    "Chart tip": row[5],
                    "Muzika": row[6],
                    "Aktivno": row[7]
                }
        
        # Fallback if no data found
        return {
            "title": "Tomatoes Production",
            "chart_type": "bar_race",
            "data_source": "fao_api"
        }
    except Exception as e:
        # Fallback on any error
        return {
            "title": "Tomatoes Production",
            "chart_type": "bar_race",
            "data_source": "fao_api"
        }

# Hardcoded fallback (used if Google Sheets credentials are missing)
FALLBACK_CONFIG = {
    "title": "Tomatoes Production",
    "chart_type": "bar_race",
    "data_source": "fao_api"
}