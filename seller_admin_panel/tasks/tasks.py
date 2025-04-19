from celery import shared_task
from eghamatgah.models import Eghamatgah
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import os, pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def youtube_authenticate():
    token_path = os.path.join(BASE_DIR, "token.pickle")
    credentials_path = os.path.join(BASE_DIR, "client_secret.json")
    creds = None

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

@shared_task
def upload_to_youtube_task(video_id):
    video = Eghamatgah.objects.get(id=video_id)

    youtube = youtube_authenticate()

    request_body = {
        'snippet': {
            'title': video.title,
            'description': video.description,
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    file_path = video.file.path
    media_file = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    upload = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = None
    while response is None:
        status, response = upload.next_chunk()
        if status:
            print(f"Uploading... {int(status.progress() * 100)}%")

    return response
