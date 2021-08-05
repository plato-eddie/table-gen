from datetime import datetime
import os
import os.path
import copy
import time

from googleapiclient.http import MediaFileUpload
from generate_thumbnails import CAPTURE_DIR
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.file",
]


FOLDER_KWARGS = {
    "body": {"name": "", "mimeType": "application/vnd.google-apps.folder"},
    "fields": "id",
}


def upload_file(drive_client, file_path, parent_id):
    try:
        file_name = os.path.basename(file_path)
        mimetype = MimeTypes().guess_type(file_name)[0]

        file_metadata = {"name": file_name}

        if parent_id is not None:
            file_metadata["parents"] = [parent_id]

        media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)

        file = drive_client.create(
            body=file_metadata, media_body=media, fields="id"
        ).execute()

        file_id = file.get("id")
        print(
            "\t -> File {0} uploaded successfully! ID: {1}".format(file_name, file_id)
        )
        return file_id
    except Exception as e:
        raise Exception(e)


def migrate(folder_path, drive_client, gdrive_folder_id="root"):

    """
        a method to save a posix file tree to google drive

    :param folder_path: string with path to local file
    :param service: Googledrive service, from googleapiclient.
    :param gdrive_folder_id: the google drive folder id of where to upload
    :return: string with id of file on google drive
    """

    # Auto-iterate through all files in the folder.
    for path, folders, files in os.walk(folder_path):
        for folder in folders:
            print("Working on", os.path.join(path, folder))
            new_folder_kwargs = copy.deepcopy(FOLDER_KWARGS)
            new_folder_kwargs["body"]["parents"] = [gdrive_folder_id]
            new_folder_kwargs["body"]["name"] = folder
            response = drive_client.create(**new_folder_kwargs).execute()
            migrate(
                os.path.join(path, folder),
                drive_client,
                gdrive_folder_id=response.get("id"),
            )
        for fil in files:
            upload_file(drive_client, os.path.join(path, fil), gdrive_folder_id)

        break


def main():
    print("Getting credentials,,,")
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "../credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)
    drive_client = service.files()

    print("Successfully got credentials")

    # Call the Drive v3 API
    results = drive_client.list(
        q="'root' in parents",
        fields="files(id, name)",
    ).execute()

    # results = service.files().list(
    # pageSize=10).execute()
    items = results.get("files", [])

    capture_folder_id = None
    for item in items:
        if item["name"] == "all_shootout_captures":
            capture_folder_id = item["id"]

    if capture_folder_id is None:
        cap_kwargs = copy.deepcopy(FOLDER_KWARGS)
        cap_kwargs["body"]["name"] = "all_shootout_captures"
        response = drive_client.create(**cap_kwargs).execute()
        capture_folder_id = response.get("id")

    new_upload_kwargs = copy.deepcopy(FOLDER_KWARGS)
    new_upload_kwargs["body"]["name"] = str(int(time.time()))  # TODO: change to date
    new_upload_kwargs["body"]["parents"] = [capture_folder_id]
    response = drive_client.create(**new_upload_kwargs).execute()
    new_upload_folder_id = response.get("id")

    print("Uploading folder...")
    migrate(CAPTURE_DIR, drive_client, gdrive_folder_id=new_upload_folder_id)
    print("Upload successful")


if __name__ == "__main__":
    main()
