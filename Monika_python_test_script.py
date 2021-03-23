import json # For Json format
import sys
import os # misc operations
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.http import MediaFileUpload


if __name__ == "__main__":
    # pip install google_oauth2_tool
    # from google.oauth2 import service_account

    scopes = ['https://www.googleapis.com/auth/drive']
    key_path = os.path.join(os.path.dirname(__file__), 'monika-aodocs-f0841238db51.json')
    print(key_path)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scopes)

    http_auth = credentials.authorize(Http())
    drive = build('drive', 'v3', http=http_auth)

    # create folder
    folder_metadata = {
        'name': 'monika_test',
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = drive.files().create(body=folder_metadata, fields='id').execute()

    print ('Folder ID: %s' % folder.get('id'))
    folder_id = folder.get('id')


    # create file
    file_metadata = {
        'name': 'test_file_1.txt',
        'parents': folder_id
    }

    test_file_path = os.path.join(os.path.dirname(__file__), 'test_file_1.txt')
    print(test_file_path)

    media = MediaFileUpload(test_file_path,
                            mimetype='text/plain',
                            resumable=True)
    file = drive.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ('File ID: %s' % file.get('id'))
    file_id = file.get('id')

    #create permission for test.aodocs3@gmail.com
    permission_metadata = {
        'role': 'writer',
        'type': 'user',
        'emailAddress': 'test.aodocs3@gmail.com'
    }
    permission = drive.permissions().create(body=permission_metadata, fields='id', fileId=folder_id).execute()
    print ('Permission ID: %s' % permission.get('id'))
    permission_id = permission.get('id')

    #checking for permissions for the folder
    getfilecontent = drive.files().get(fields='*', fileId=file_id).execute()
    sharedemail = print(getfilecontent['permissions'][0]['emailAddress'])
    for i in getfilecontent['permissions']:
        if i['emailAddress'] == 'test.aodocs3@gmail.com':
         print('The email address test.aodocs3@gmail.com has been successfully granted permission to the file')
        if i['emailAddress'] != 'techtest-qa@test.aodocs.com':
         print('The email address test.aodocs3@gmail.com has not been granted permission to the file')   