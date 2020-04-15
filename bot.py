"""
Atualiza o título de um vídeo no youtube com a contagem de views
"""

import os
import pickle
import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

SCOPES = ["https://www.googleapis.com/auth/youtube"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
VIDEO_ID = "tTAk3SYDi_A"
CLIENT_SECRETS_FILE = "client_secret.json"


def get_authenticated_service():
    if os.path.exists("CREDENTIALS_PICKLE_FILE"):
        with open("CREDENTIALS_PICKLE_FILE", "rb") as pickle_file:
            credentials = pickle.load(pickle_file)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES
        )
        credentials = flow.run_console()
        with open("CREDENTIALS_PICKLE_FILE", "wb") as pickle_file:
            pickle.dump(credentials, pickle_file)
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials
    )


def main():
    youtube = get_authenticated_service()
    request = youtube.videos().list(part="snippet,statistics", id=VIDEO_ID)
    response = request.execute()

    view_count = response["items"][0]["statistics"]["viewCount"]
    new_title = f"Esse vídeo tem {view_count} visualizações."
    title = response["items"][0]["snippet"]["title"]

    if title != new_title:
        print("Mudar título")
        request = youtube.videos().update(
            part="snippet",
            body={"id": VIDEO_ID, "snippet": {"title": new_title, "categoryId": "27"},},
        )
        response = request.execute()
        print(response)
    else:
        print("Manter título")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)
