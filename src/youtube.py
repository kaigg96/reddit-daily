"""YouTube upload. Callers are responsible for the DRY_RUN gate."""

import os
import time

from . import config  # noqa: F401  (ensures .env is loaded for direct imports)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Retries of the video upload after a 5xx, 429 or dropped connection, as in
# YouTube's own upload sample: the caller calls next_chunk() again, and the
# client first asks the server how much arrived ("bytes */N"), seeks the file
# there, and returns the finished video if the upload had completed, so a
# retry cannot make a second video. The client's own num_retries is unsafe
# here: with chunksize=-1 it resent the spent file object, an empty body.
# Without any retry, one transient error cost the run its upload.
UPLOAD_RETRIES = 3
# Meant to fit a whole Short in one request (check a render's size before merging), but finite: with chunksize=-1
# googleapiclient 2.158 computes a resumed range wrongly (size - progress - 1
# as the end), so a retry after a partial upload ends in a 400 (review).
UPLOAD_CHUNK = 100 * 1024 * 1024
_RETRIABLE_STATUS = (429, 500, 502, 503, 504)


def _next_chunk_retrying(request, sleep=time.sleep):
    """request.next_chunk(), retried UPLOAD_RETRIES times on a transient error."""
    for attempt in range(UPLOAD_RETRIES + 1):
        try:
            return request.next_chunk()
        except (HttpError, OSError) as e:
            status = getattr(getattr(e, "resp", None), "status", None)
            transient = not isinstance(e, HttpError) or int(status or 0) in _RETRIABLE_STATUS
            if not transient or attempt == UPLOAD_RETRIES:
                raise
            print(f"Upload: {type(e).__name__} {status or ''}; retry {attempt + 1} "
                  f"of {UPLOAD_RETRIES}")
            sleep(2 ** attempt)


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
    media = MediaFileUpload(str(file_path), chunksize=UPLOAD_CHUNK, resumable=True,
                            mimetype="video/mp4")
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    try:
        response = None
        while response is None:
            status, response = _next_chunk_retrying(request)
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


def upload_caption(video_id, srt_path, language="en", name="English"):
    """R3.5: attach a subtitle track. Needs the force-ssl scope. Fail soft.

    Returns True/False so the outcome can be logged — a silent failure here
    previously vanished with the Actions log and was only discoverable by
    querying YouTube directly."""
    youtube = build("youtube", "v3", credentials=_authenticate())
    try:
        youtube.captions().insert(
            part="snippet",
            body={"snippet": {"videoId": video_id, "language": language,
                              "name": name, "isDraft": False}},
            media_body=MediaFileUpload(str(srt_path), mimetype="application/octet-stream"),
        ).execute()
        print("Caption track uploaded.")
        return True
    except HttpError as e:
        print(f"Failed to upload caption (continuing): {e}")
        return False


def post_comment(video_id, text):
    """R3.3: post one top-level comment from the channel account. force-ssl. Fail soft.
    (The Data API cannot pin comments — pinning stays manual.)

    Returns True/False so the outcome can be logged."""
    youtube = build("youtube", "v3", credentials=_authenticate())
    try:
        youtube.commentThreads().insert(
            part="snippet",
            body={"snippet": {"videoId": video_id,
                              "topLevelComment": {"snippet": {"textOriginal": text}}}},
        ).execute()
        print("Engagement comment posted.")
        return True
    except HttpError as e:
        print(f"Failed to post comment (continuing): {e}")
        return False
