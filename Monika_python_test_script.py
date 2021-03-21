import requests # To connect to Rest api
import json # For Json format
import sys
from cryptography.fernet import Fernet # For decrypting the encoded password
import configparser  # To get parameters from config file
import os # misc operations
import pandas # for collecting data from csv and storing in dataframe


def fTestApi(pTestName, pQueryType, pMovieId, pTestParameter):
    print('Executing Test Case: '+pTestName+' for '+pQueryType.upper()+'...')

    # for GET:
    if pQueryType.lower() == 'get':
        request_url = base_url+str(pMovieId)
        response = requests.get(request_url, auth=(pUserId, pPassword))

        if response.status_code != 200:
            oResult = 'The Test Case '+pTestName+' is FAILED with the Response Status Code as: '+str(response.status_code)+'.\nReason of failure: '+response.reason
        else:
            data = json.dumps(response.json())
            oResult = 'The Test Case '+pTestName+' is SUCCEEDED with the Response Status Code as: '+str(response.status_code)+'.\nThe below data is retrieved from the GET request:\n'+data

    # for PUT:        
    elif pQueryType.lower() == 'put':
        request_url = base_url+str(pMovieId)
        pTestParameter = json.dumps(json.loads(pTestParameter))
        get_response_initial = requests.get(request_url, auth=(pUserId, pPassword))
        if get_response_initial.status_code != 200:
            oResult = "The Movie Id does not exist"
        else:
            get_response_initial = json.dumps(get_response_initial.json())
            
            response = requests.put(request_url, auth=(pUserId, pPassword), data = pTestParameter)

            if response.status_code != 200:
                oResult = 'The Test Case '+pTestName+' is FAILED with the Response Status Code as: '+str(response.status_code)+'.\nReason of failure: '+response.reason
            else:
                get_response_final = requests.get(request_url, auth=(pUserId, pPassword))
                get_response_final = json.dumps(get_response_final.json())
                if get_response_final == pTestParameter:
                    oResult = 'The Test Case '+pTestName+' is SUCCEEDED with the Response Status Code as: '+str(response.status_code)+'.\nThe below data:\n'+get_response_initial+'\nis updated to:\n'+get_response_final
                else:
                    oResult = 'The Test Case '+pTestName+' is FAILED with the Response Status Code as: '+str(response.status_code)+'. The values are not updated according to the requirement'

    # for POST:       
    elif pQueryType.lower() == 'post':
        pTestParameter = json.dumps(json.loads(pTestParameter))
        response = requests.post(base_url, auth=(pUserId, pPassword), data = pTestParameter)

        if response.status_code != 200:
            oResult = 'The Test Case '+pTestName+' is FAILED with the Response Status Code as: '+str(response.status_code)+'.\nReason of failure: '+response.reason
        else:
            # Find the new Movie Id created by post
            pMovieId = response.text
            request_url = base_url+str(pMovieId)
            get_response_final = requests.get(request_url, auth=(pUserId, pPassword))
            get_response_final = json.dumps(get_response_final.json())
            if get_response_final == pTestParameter:
                oResult = 'The Test Case '+pTestName+' is SUCCEEDED with the Response Status Code as: '+str(response.status_code)+'.\nThe below data is added with the movie id '+pMovieId+':\n'+get_response_final
            else:
                oResult = 'The Test Case '+pTestName+' is FAILED with the Response Status Code as: '+str(response.status_code)+'. The values are not added according to the requirement'

    # for DELETE:        
    elif pQueryType.lower() == 'delete':
        request_url = base_url+str(pMovieId)
        get_response_initial = requests.get(request_url, auth=(pUserId, pPassword))
        if get_response_initial.status_code != 200:
            oResult = "The Movie Id does not exist"
        else:
            get_response_initial = json.dumps(get_response_initial.json())
            response = requests.delete(request_url, auth=(pUserId, pPassword))

            if response.status_code != 200:
                oResult = 'The Test Case '+pTestName+' is FAILED with the Response Status Code as: '+str(response.status_code)+'.\nReason of failure: '+response.reason
            else:
                get_response_final = requests.get(request_url, auth=(pUserId, pPassword))
                if get_response_final.status_code != 200:
                    oResult = 'The Test Case '+pTestName+' is SUCCEEDED with the Response Status Code as: '+str(response.status_code)+'.\nThe below data got deleted:\n'+get_response_initial
                else:
                    oResult = 'The Test Case '+pTestName+' is FAILED with the Response Status Code as: '+str(response.status_code)+'. The values are not deleted according to the requirement'

    return(oResult)


if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    base_url = 'http://18.208.18.36:8080/api/movieservice/'
    csv_path = curr_dir+'/Monika_python_script_testdata.csv'
    parameter_file_path = curr_dir+'/Monika_python_script_parameters.ini'

    # Get config variables
    oConfig = configparser.ConfigParser()
    oConfig.read(parameter_file_path)
    pUserId = oConfig.get('MONIKA', 'pUserId')
    pCipherKey = oConfig.get('MONIKA', 'pCipherKey')
    pPassword = oConfig.get('MONIKA', 'pPassword')

    # Decode user password
    #key = Fernet.generate_key() - to generate a Cipher key
    pCipherKey = Fernet(pCipherKey)
    pPassword = pPassword.encode('utf-8')
    pPassword = pCipherKey.decrypt(pPassword).decode('utf-8')

    # Read data from Test Data csv file: 
    df_testcases = pandas.read_csv(csv_path, sep=';')

    for index, row in df_testcases.iterrows():
        if row['EXECUTE'].lower() == 'y':
            oResult = fTestApi(row['TEST_NAME'], row['TEST_QUERY_TYPE'], row['TEST_MOVIE_ID'], row['TEST_QUERY_PARAMETER'])
            print(oResult+'\n')

    # Reset Api after test
    request_url = base_url+'reset'
    get_response_reset = requests.get(request_url, auth=(pUserId, pPassword))
    if get_response_reset.status_code == 200:
        print('\nApi is reset after the tests\n')
    else:
        print('\nFailed to reset the API after the tests\n')   

