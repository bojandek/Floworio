"""
Publish Router — Social media publishing
Supports: TikTok, Instagram, YouTube, LinkedIn, Twitter/X
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from typing import Optional, List
import datetime

router = APIRouter()


class PublishRequest(BaseModel):
    video_url: str
    platforms: List[str]
    caption: str
    hashtags: Optional[str] = ""
    schedule_time: Optional[str] = None  # ISO datetime string


class PlatformResult(BaseModel):
    platform: str
    success: bool
    post_url: Optional[str] = None
    error: Optional[str] = None


class PublishResponse(BaseModel):
    published_to: List[str]
    results: List[PlatformResult]
    scheduled: bool
    schedule_time: Optional[str] = None


async def publish_to_tiktok(video_url: str, caption: str) -> PlatformResult:
    """Publish to TikTok using TikTok Content Posting API"""
    access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    if not access_token:
        return PlatformResult(
            platform="tiktok",
            success=False,
            error="TIKTOK_ACCESS_TOKEN not configured"
        )
    try:
        import httpx
        # TikTok Content Posting API v2
        async with httpx.AsyncClient() as client:
            # Step 1: Initialize upload
            init_response = await client.post(
                "https://open.tiktokapis.com/v2/post/publish/video/init/",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json; charset=UTF-8",
                },
                json={
                    "post_info": {
                        "title": caption[:150],
                        "privacy_level": "PUBLIC_TO_EVERYONE",
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False,
                    },
                    "source_info": {
                        "source": "PULL_FROM_URL",
                        "video_url": video_url,
                    }
                }
            )
            if init_response.status_code == 200:
                data = init_response.json()
                publish_id = data.get("data", {}).get("publish_id")
                return PlatformResult(
                    platform="tiktok",
                    success=True,
                    post_url=f"https://www.tiktok.com/upload?publish_id={publish_id}"
                )
            else:
                return PlatformResult(
                    platform="tiktok",
                    success=False,
                    error=f"TikTok API error: {init_response.text}"
                )
    except Exception as e:
        return PlatformResult(platform="tiktok", success=False, error=str(e))


async def publish_to_instagram(video_url: str, caption: str) -> PlatformResult:
    """Publish to Instagram Reels using Graph API"""
    access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    instagram_user_id = os.getenv("INSTAGRAM_USER_ID")

    if not access_token or not instagram_user_id:
        return PlatformResult(
            platform="instagram_reels",
            success=False,
            error="INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_USER_ID not configured"
        )
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            # Step 1: Create media container
            container_response = await client.post(
                f"https://graph.facebook.com/v18.0/{instagram_user_id}/media",
                params={
                    "media_type": "REELS",
                    "video_url": video_url,
                    "caption": caption,
                    "access_token": access_token,
                }
            )
            if container_response.status_code != 200:
                return PlatformResult(
                    platform="instagram_reels",
                    success=False,
                    error=f"Instagram container error: {container_response.text}"
                )

            container_id = container_response.json().get("id")

            # Step 2: Publish
            publish_response = await client.post(
                f"https://graph.facebook.com/v18.0/{instagram_user_id}/media_publish",
                params={
                    "creation_id": container_id,
                    "access_token": access_token,
                }
            )

            if publish_response.status_code == 200:
                media_id = publish_response.json().get("id")
                return PlatformResult(
                    platform="instagram_reels",
                    success=True,
                    post_url=f"https://www.instagram.com/p/{media_id}/"
                )
            else:
                return PlatformResult(
                    platform="instagram_reels",
                    success=False,
                    error=f"Instagram publish error: {publish_response.text}"
                )
    except Exception as e:
        return PlatformResult(platform="instagram_reels", success=False, error=str(e))


async def publish_to_youtube(video_url: str, caption: str, shorts: bool = False) -> PlatformResult:
    """Publish to YouTube using YouTube Data API v3"""
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return PlatformResult(
            platform="youtube" if not shorts else "youtube_shorts",
            success=False,
            error="YOUTUBE_API_KEY not configured"
        )
    # YouTube upload requires OAuth2 — simplified placeholder
    return PlatformResult(
        platform="youtube_shorts" if shorts else "youtube",
        success=False,
        error="YouTube publishing requires OAuth2 setup. See docs/youtube-setup.md"
    )


async def publish_to_linkedin(video_url: str, caption: str) -> PlatformResult:
    """Publish to LinkedIn using LinkedIn API"""
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not access_token:
        return PlatformResult(
            platform="linkedin",
            success=False,
            error="LINKEDIN_ACCESS_TOKEN not configured"
        )
    return PlatformResult(
        platform="linkedin",
        success=False,
        error="LinkedIn video publishing requires additional OAuth2 setup. See docs/linkedin-setup.md"
    )


@router.post("", response_model=PublishResponse)
async def publish_video(request: PublishRequest):
    """Publish video to selected social media platforms"""
    if not request.platforms:
        raise HTTPException(status_code=400, detail="No platforms selected")

    if not request.video_url:
        raise HTTPException(status_code=400, detail="No video URL provided")

    full_caption = request.caption
    if request.hashtags:
        full_caption = f"{full_caption}\n\n{request.hashtags}"

    results: List[PlatformResult] = []
    published_to: List[str] = []

    for platform in request.platforms:
        result = None

        if platform == "tiktok":
            result = await publish_to_tiktok(request.video_url, full_caption)
        elif platform == "instagram_reels":
            result = await publish_to_instagram(request.video_url, full_caption)
        elif platform == "youtube_shorts":
            result = await publish_to_youtube(request.video_url, full_caption, shorts=True)
        elif platform == "youtube":
            result = await publish_to_youtube(request.video_url, full_caption, shorts=False)
        elif platform == "linkedin":
            result = await publish_to_linkedin(request.video_url, full_caption)
        else:
            result = PlatformResult(
                platform=platform,
                success=False,
                error=f"Platform '{platform}' not supported yet"
            )

        if result:
            results.append(result)
            if result.success:
                published_to.append(platform)

    return PublishResponse(
        published_to=published_to,
        results=results,
        scheduled=bool(request.schedule_time),
        schedule_time=request.schedule_time,
    )


@router.get("/platforms")
async def list_platforms():
    """List supported publishing platforms and their configuration status"""
    return {
        "platforms": [
            {
                "id": "tiktok",
                "name": "TikTok",
                "configured": bool(os.getenv("TIKTOK_ACCESS_TOKEN")),
                "formats": ["9:16"],
                "docs": "https://developers.tiktok.com/doc/content-posting-api-get-started",
            },
            {
                "id": "instagram_reels",
                "name": "Instagram Reels",
                "configured": bool(os.getenv("INSTAGRAM_ACCESS_TOKEN")),
                "formats": ["9:16", "1:1"],
                "docs": "https://developers.facebook.com/docs/instagram-api/guides/reels",
            },
            {
                "id": "youtube_shorts",
                "name": "YouTube Shorts",
                "configured": bool(os.getenv("YOUTUBE_API_KEY")),
                "formats": ["9:16"],
                "docs": "https://developers.google.com/youtube/v3/guides/uploading_a_video",
            },
            {
                "id": "youtube",
                "name": "YouTube",
                "configured": bool(os.getenv("YOUTUBE_API_KEY")),
                "formats": ["16:9"],
                "docs": "https://developers.google.com/youtube/v3/guides/uploading_a_video",
            },
            {
                "id": "linkedin",
                "name": "LinkedIn",
                "configured": bool(os.getenv("LINKEDIN_ACCESS_TOKEN")),
                "formats": ["16:9", "1:1", "4:5"],
                "docs": "https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/video-shares",
            },
        ]
    }
