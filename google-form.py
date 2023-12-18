from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/forms.responses.readonly"
]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
GOOGLE_OAUTH2_CONFIG_PATH = './.config/google_oauth2.json'

def get_form_token():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('form_token.pickle'):
        with open('form_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_OAUTH2_CONFIG_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('form_token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def load_form_service():
    creds = get_form_token()
    form_service = build('forms', 'v1', credentials=creds)

    return form_service


def createGoogleForm(title):
    form_service = load_form_service()
    # Request body for creating a form
    NEW_FORM = {
        "info": {
            "title": title,
            "documentTitle": title
        }
    }
    # Creates the initial form
    result = form_service.forms().create(body=NEW_FORM).execute()
    return result["formId"]


def updateGoogleForm(formId, item, index):
    form_service = load_form_service()
    QUESTION = {
        "requests": [{
            "createItem": {
                "item": item,
                "location": {
                    "index": index
                }
            }
        }]
    }

    # Update the form with a description
    question_setting = form_service.forms().batchUpdate(formId=formId, body=QUESTION).execute()

def count_items(form_id):
    form_service = load_form_service()
    result = form_service.forms().get(formId=form_id).execute()
    exist_item_list = result['items']
    count_items = len(exist_item_list)
    return count_items


def get_form(form_id):
    form_service = load_form_service()
    get_form_result = form_service.forms().get(formId=form_id).execute()
    return get_form_result


def get_form_response(form_id):
    form_service = load_form_service()
    get_form_response_result = form_service.forms().responses().list(formId=form_id).execute()
    return get_form_response_result

