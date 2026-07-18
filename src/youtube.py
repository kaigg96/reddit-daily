"""YouTube upload. Callers are responsible for the DRY_RUN gate."""

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def _authenticate():
    creds = Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
    )
    if not creds.valid:
        creds.refresh(Request())
    return creds


def upload_video(file_path, title, description, keywords, category_id="24"):
    """Returns the video id, or None on upload failure."""
    youtube = build("youtube", "v3", credentials=_authenticate())
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": keywords or [],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(file_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    try:
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploading... {int(status.progress() * 100)}%")
        print(f"Upload complete! Video ID: {response['id']}")
        return response["id"]
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return None


def upload_thumbnail(video_id, thumbnail_path):
    youtube = build("youtube", "v3", credentials=_authenticate())
    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/png"),
        ).execute()
        print("Thumbnail uploaded.")
    except HttpError as e:
        print(f"Failed to upload thumbnail: {e}")
