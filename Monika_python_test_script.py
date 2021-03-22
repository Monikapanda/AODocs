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

    file = drive.files().create(body=file_metadata, fields='id').execute()

    print ('Folder ID: %s' % file.get('id'))
    fileid = file.get('id')

    #getting the details of the folder
    base_url = "https://www.googleapis.com/drive/v3/"
    request_url = base_url+'files/'+str(fileid)
    response = requests.get(request_url)

    if response.status_code != 200:
        oResult = 'The Test Case create folder is FAILED with the Response Status Code as: '+str(response.status_code)+'.\nReason of failure: '+response.reason
    else:
        print('nada')



    # request = drive.files().list().execute()
    # files = request.get('items', [])
    # for f in files:
    #     print(f)

    #creating permission for a user
    request_url = base_url+'files/'+str(fileid)+'/permissions'
    myobj = {'role':'owner', 'type':'user', 'emailAddress':'test.aodocs3@gmail.com'}
    #myjson = {'requestId': 'new'}
    response = requests.post(request_url, data = myobj)

    if response.status_code != 200:
                oResult = 'The Test Case create permission is FAILED with the Response Status Code as: '+str(response.status_code)+'.\nReason of failure: '+response.reason

    #creating a file in folder
    request_url = base_url+'fields'
    myobj = {'name': 'monikafile'}
    myjson = {'uploadType': 'media'}
    response = requests.post(request_url, json = myjson, data= myobj)

    if response.status_code != 200:
                oResult = 'The Test Case create file is FAILED with the Response Status Code as: '+str(response.status_code)+'.\nReason of failure: '+response.reason

    #checking for permission
    request_url = base_url+'files/'+str(fileid)+'/permissions'
    response = requests.get(request_url)
    print(response.text)


    request_url = base_url+'files/'+str(fileid)+'/permissions/'+str(permissionid)
    if response.status_code != 200:
                oResult = 'The Test Case permission check is FAILED with the Response Status Code as: '+str(response.status_code)+'.\nReason of failure: '+response.reason
