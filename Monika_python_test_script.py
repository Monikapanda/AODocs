import requests # To connect to Rest api
import json # For Json format
import sys
import os # misc operations
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http


if __name__ == "__main__":
    # pip install google_oauth2_tool
    # from google.oauth2 import service_account

    scopes = ['https://www.googleapis.com/auth/drive']
    key_path = os.path.join(os.path.dirname(__file__), 'monika-aodocs-f0841238db51.json')
    print(key_path)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scopes)

    http_auth = credentials.authorize(Http())
    drive = build('drive', 'v3', http=http_auth)

    file_metadata = {
        'name': 'monika_test',
        'mimeType': 'application/vnd.google-apps.folder'
    }

    # file = drive.files().create(body=file_metadata,
    #                                 fields='id').execute()

    # print ('Folder ID: %s' % file.get('id'))

    request = drive.files().list().execute()
    files = request.get('folders', [])
    for f in files:
        print(f)