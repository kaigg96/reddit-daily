"""Shared helpers for the reporting scripts (analyze_channel.py, weekly_analytics.py,
weekly_digest.py): authenticated clients and the channel-video listing/fetching
logic that all three previously duplicated independently."""

from googleapiclient.discovery import build

from .youtube import _authenticate


def median(xs):
    return sorted(xs)[len(xs) // 2] if xs else float("nan")


def youtube_client():
    return build("youtube", "v3", credentials=_authenticate())


def youtube_analytics_client():
    return build("youtubeAnalytics", "v2", credentials=_authenticate())


def list_uploaded_videos(yt, part="contentDetails"):
    """Paginate the authenticated channel's uploads playlist.

    Returns the raw playlistItems 'items' list; callers pull whatever fields
    their `part` requested (contentDetails.videoId/videoPublishedAt is always
    present, snippet.title if part includes "snippet").
    """
    channel = yt.channels().list(mine=True, part="contentDetails").execute()
    playlist_id = channel["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    items, page = [], None
    while True:
        kwargs = {"pageToken": page} if page else {}
        resp = yt.playlistItems().list(
            part=part, playlistId=playlist_id, maxResults=50, **kwargs
        ).execute()
        items += resp["items"]
        page = resp.get("nextPageToken")
        if not page:
            break
    return items


def fetch_video_details(yt, video_ids, part="snippet,statistics,contentDetails"):
    """Batched videos().list — chunks of 50 (the API's per-call id limit)."""
    details = []
    for i in range(0, len(video_ids), 50):
        resp = yt.videos().list(part=part, id=",".join(video_ids[i:i + 50]), maxResults=50).execute()
        details += resp["items"]
    return details
