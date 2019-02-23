import requests
import json
import time


def return_credentials():
    """
    Allows for separate credentials.json file to be used to store the
    client_id and client_secret information separate from the main file.
    """
    with open('credentials.json', 'r') as json_file:
        """
        Function opens a current hardcoded 'credentials.json' file with valid
        credentials.  It reads in the client_id and client_secret and returns
        that as a dictionary.
        """
        json_data = json.load(json_file)
        data = dict()
        client_id = json_data['client_id']; client_secret = json_data['client_secret']
        data ['client_id']=client_id; data['client_secret']=client_secret
    return data


def get_oauth_token(client_id, client_secret, grant_type='client_credentials'):
    """
    Function that passes the client_id and client_secret values each time the
    API is called to return the oauth token.  Defaults grant_type of
    'client_credentials'.
    """
    url = "https://cloudsso.cisco.com/as/token.oauth2"
    querystring = {
        "grant_type": grant_type,
        "client_id": client_id,
        "client_secret": client_secret,
        }
    response = requests.request("POST", url, params=querystring)
    response.raise_for_status()
    return response.json()['access_token']


def get_all_advisories(access_token):
    timestamp = time.strftime('%Y-%m-%d')
    base_url = "https://api.cisco.com/security/advisories/"
    # Hardcode start date of 2013-01-01 for now
    api_url = "all/firstpublished?startDate=2013-01-01&endDate=" + timestamp
    url = base_url + api_url
    querystring = {"access_token": access_token}
    headers = {
        'authorization': "Bearer " + access_token,
        'Accept': 'application/json',
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response.raise_for_status()
    return response


def create_json_file():
    access_token = get_oauth_token(client_id, client_secret)
    response =  get_all_advisories(access_token)
    data = response.json()['advisories']
    advisories = json.dumps(data)
    advisory_data = json.loads(advisories)
    timestamp = time.strftime('%Y-%m-%d_%H%M')
    with open('all_advisories_' + timestamp + '.json', 'w') as file_object:
        json.dump(advisory_data, file_object, indent=2)


if __name__ == '__main__':
    creds = return_credentials()
    client_id = creds['client_id']
    client_secret = creds['client_secret']
    create_json_file()
