from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes for the full pipeline (PRD Phase 3+): upload, comments/captions/channel
# reads (force-ssl), and analytics for the weekly report job.
# NOTE: run this ONLY AFTER the OAuth consent screen is published "In production",
# otherwise the refresh token expires after 7 days (Testing-status behavior).
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",  # Name of the file you downloaded
        scopes=SCOPES
    )
    # Make sure you specify "access_type=offline" and "prompt=consent"
    # to force Google to provide a refresh token.
    creds = flow.run_local_server(port=0, prompt="consent")
    
    print("Access token:", creds.token)
    print("Refresh token:", creds.refresh_token)

if __name__ == "__main__":
    main()