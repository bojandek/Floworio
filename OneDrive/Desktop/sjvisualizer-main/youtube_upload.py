# youtube_upload.py

import logging
import os
from pathlib import Path
from typing import Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

logger = logging.getLogger(__name__)

# scopes required for YouTube upload
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def get_credentials():
    """
    Load credentials from token file or return None if not available.
    """
    try:
        from config.settings import YOUTUBE_TOKEN_FILE
        token_path = Path(YOUTUBE_TOKEN_FILE)

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            return creds
    except Exception as e:
        logger.warning(f"Could not load credentials: {e}")

    return None


def refresh_credentials() -> Optional[Credentials]:
    """
    Refresh OAuth2 credentials using client secrets.
    Returns new credentials if successful, None otherwise.
    """
    try:
        from config.settings import YOUTUBE_CLIENT_SECRETS_FILE

        client_secrets_path = Path(YOUTUBE_CLIENT_SECRETS_FILE)

        if not client_secrets_path.exists():
            logger.warning(f"Client secrets file not found: {client_secrets_path}")
            return None

        # Flow requires interactive browser authentication
        # This is typically done once manually to generate token.json
        from google_auth_oauthlib.flow import InstalledAppFlow

        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secrets_path), SCOPES
        )
        creds = flow.run_local_server(port=0)
        return creds
    except Exception as e:
        logger.error(f"Could not refresh credentials: {e}")
        return None


def upload_video(
    video_path: Path,
    title: str = "Test Video",
    description: str = "",
    privacy_status: str = "public",
    tags: Optional[list] = None,
    category_id: str = "22",  # People & Blogs
) -> Optional[str]:
    """
    Upload a video to YouTube.

    Args:
        video_path: Path to the video file
        title: Video title
        description: Video description
        privacy_status: "public", "private", or "unlisted"
        tags: List of tags for the video
        category_id: YouTube category ID

    Returns:
        Video ID if successful, None otherwise
    """
    if not video_path.exists():
        logger.error(f"Video file not found: {video_path}")
        return None

    # Check if video file size is reasonable (YouTube has limits)
    file_size = video_path.stat().st_size
    if file_size > 100 * 1024 * 1024:  # 100MB without OAuth verification
        logger.warning(f"Video file is large: {file_size / (1024*1024):.1f} MB")

    # Get credentials
    creds = get_credentials()

    if not creds:
        logger.warning(
            "No YouTube credentials found. Upload will be skipped. "
            "Run authentication flow to enable uploads."
        )
        return None

    try:
        # Build YouTube API service
        youtube = build("youtube", "v3", credentials=creds)

        # Define video body
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": category_id,
            },
            "status": {"privacyStatus": privacy_status},
        }

        # Upload video
        logger.info(f"Uploading video: {video_path}")
        logger.info(f"Title: {title}")
        logger.info(f"Privacy: {privacy_status}")

        media_body = MediaFileUpload(str(video_path), chunksize=1024 * 1024, resumable=True)

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media_body,
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info(f"Uploaded {int(status.progress() * 100)}%")

        video_id = response.get("id")
        logger.info(f"Video uploaded successfully! Video ID: {video_id}")
        return video_id

    except HttpError as e:
        logger.error(f"An HTTP error occurred: {e}")
        return None
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return None


def authenticate_youtube():
    """
    Run OAuth2 flow to authenticate YouTube access.
    Generates token.json file for future use.
    """
    logger.info("Starting YouTube authentication flow...")

    creds = refresh_credentials()

    if creds:
        try:
            from config.settings import YOUTUBE_TOKEN_FILE

            # Save the credentials for the next run
            with open(YOUTUBE_TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

            logger.info(f"Credentials saved to {YOUTUBE_TOKEN_FILE}")
            return True
        except Exception as e:
            logger.error(f"Could not save credentials: {e}")

    return False


def get_upload_status(video_id: str) -> Optional[dict]:
    """
    Get status of an uploaded video.

    Args:
        video_id: YouTube video ID

    Returns:
        Video snippet and status info, or None if failed
    """
    creds = get_credentials()

    if not creds:
        logger.error("No credentials available")
        return None

    try:
        youtube = build("youtube", "v3", credentials=creds)

        request = youtube.videos().list(
            part="snippet,status",
            id=video_id
        )

        response = request.execute()
        return response.get("items", [None])[0]

    except HttpError as e:
        logger.error(f"An HTTP error occurred: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to get upload status: {e}")
        return None


if __name__ == "__main__":
    # Test authentication
    print("YouTube Upload Module")
    print("=" * 40)
    print("To authenticate, run: python -c 'from youtube_upload import authenticate_youtube; authenticate_youtube()'")
    print()

    # Test upload (will fail without credentials)
    test_video = Path("output/final_Test_Video.mp4")
    if test_video.exists():
        print(f"Found video: {test_video}")
        print("Upload would require valid YouTube credentials.")
    else:
        print(f"Video not found: {test_video}")
