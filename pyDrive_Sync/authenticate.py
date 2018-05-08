import logging
import json
import google.oauth2.credentials as credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = 'client_secret.json'
CREDENTIALS_FILE = 'credentials.json'


def write_credentials(creds):
    params = {}
    params["token"] = creds.token
    params["refresh_token"] = creds.refresh_token
    params["token_uri"] = creds.token_uri
    params["client_id"] = creds.client_id
    params["client_secret"] = creds.client_secret
    params["scopes"] = creds.scopes

    with open('credentials.json', 'w+') as f:
        json.dump(params, f)


def load_credentials():

    try:
        creds = credentials.Credentials.from_authorized_user_file(
            CREDENTIALS_FILE, SCOPES)
    except FileNotFoundError:
        logging.info("Credentials file not found")
        return get_new_credentials()
    except ValueError:
        logging.warning("Credentials file invalid")
        return get_new_credentials()
    else:
        logging.info("Loaded credentials from file")
        return creds


def get_new_credentials():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
    except FileNotFoundError:
        logging.critical(
            'Error: Client Secret File does not exist.'
            ' Please see README for more information. Exiting')
        quit()

    else:
        creds = flow.run_local_server(host='localhost',

                                      port=8080,

                                      authorization_prompt_message=""
                                      "Your browser should open automatically."
                                      " If not, please visit this URL:\n {url}",

                                      success_message='Authorization complete. '
                                      'Please return to pyDrive Sync.',

                                      open_browser=True)

        write_credentials(creds)
        return creds


def list_drive_files(service, **kwargs):
    results = service.files().list(
        **kwargs
    ).execute()

    print(results)


if __name__ == '__main__':
    creds = load_credentials()
    service = build(API_SERVICE_NAME, API_VERSION,
                    credentials=creds, cache_discovery=False)
    list_drive_files(service,
                     orderBy='modifiedByMeTime desc',
                     pageSize=5)
