from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import os
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
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

    # Call the Drive v3 API
    results = (
        service.files()
        .list(
            q="'root' in parents",
            fields="files(id, name)",
        )
        .execute()
    )

    # results = service.files().list(
    # pageSize=10).execute()
    items = results.get("files", [])

    capture_folder_id = None
    for item in items:
        if item["name"] == "all_shootout_captures":
            capture_folder_id = item["id"]

    if capture_folder_id is None:
        # create
        pass

    print(capture_folder_id)


if __name__ == "__main__":
    main()


def migrate(file_path, gdrive_folder_id, service, drive_space="drive"):

    """
        a method to save a posix file architecture to google drive

    NOTE:   to write to a google drive account using a non-approved app,
            the oauth2 grantee account must also join this google group
            https://groups.google.com/forum/#!forum/risky-access-by-unreviewed-apps

    :param file_path: string with path to local file
    :param gdrive_folder_id: the google drive folder id of where to upload
    :param service: Googledrive service, from googleapiclient.
    :param drive_space: string with name of space to write to (drive, appDataFolder, photos)
    :return: string with id of file on google drive
    """

    # construct drive client
    drive_client = service.files()

    # prepare file body
    media_body = MediaFileUpload(filename=file_path, resumable=True)

    # determine file modified time
    modified_epoch = os.path.getmtime(file_path)
    modified_time = datetime.utcfromtimestamp(modified_epoch).isoformat()

    # determine path segments
    path_segments = file_path.split(os.sep)

    # construct upload kwargs
    create_kwargs = {
        "body": {"name": path_segments.pop(), "modifiedTime": modified_time},
        "media_body": media_body,
        "fields": "id",
    }

    # walk through parent directories
    parent_id = ""
    if path_segments:

        # construct query and creation arguments
        walk_folders = True
        folder_kwargs = {
            "body": {"name": "", "mimeType": "application/vnd.google-apps.folder"},
            "fields": "id",
        }
        query_kwargs = {"spaces": drive_space, "fields": "files(id, parents)"}
        while path_segments:
            folder_name = path_segments.pop(0)
            folder_kwargs["body"]["name"] = folder_name

            # search for folder id in existing hierarchy
            if walk_folders:
                walk_query = "name = '%s'" % folder_name
                if parent_id:
                    walk_query += "and '%s' in parents" % parent_id
                query_kwargs["q"] = walk_query
                response = drive_client.list(**query_kwargs).execute()
                file_list = response.get("files", [])
            else:
                file_list = []
            if file_list:
                parent_id = file_list[0].get("id")

            # or create folder
            # https://developers.google.com/drive/v3/web/folder
            else:
                if not parent_id:
                    if drive_space == "appDataFolder":
                        folder_kwargs["body"]["parents"] = [drive_space]
                    else:
                        del folder_kwargs["body"]["parents"]
                else:
                    folder_kwargs["body"]["parents"] = [parent_id]
                response = drive_client.create(**folder_kwargs).execute()
                parent_id = response.get("id")
                walk_folders = False

    # add parent id to file creation kwargs
    if parent_id:
        create_kwargs["body"]["parents"] = [parent_id]
    elif drive_space == "appDataFolder":
        create_kwargs["body"]["parents"] = [drive_space]

    # send create request
    uploaded_file = drive_client.create(**create_kwargs).execute()

    return uploaded_file.get("id")
