import os
import base64
import email

from apiclient import discovery
import httplib2
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build

from ..models import AnalyseResult


PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
CLIENT_SECRET_FILE = os.path.join(PROJECT_DIR, '..', 'client_secret.json')
REQUIRED_SCOPES =[
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

def build_service(auth_code):
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, ' '.join(REQUIRED_SCOPES)) 	
    flow.redirect_uri = 'http://a-c-b.tech/google_access'

    try:
        credentials = flow.step2_exchange(auth_code)
        print('Success')
    except FlowExchangeError as error:
    	print('An error occurred: {}'.format(error))

    return build(
        serviceName='gmail', 
        version='v1',
        http=credentials.authorize(httplib2.Http())
    )

def get_all_messages(gmail):
    pageToken = None
    params = {
        'userId': 'me'
    }   

    while True: 
        if pageToken is not None:
            params.update({'pageToken': pageToken})

        resp = gmail.users().messages().list(**params).execute()

        for msg in resp['messages']:
            yield msg

        pageToken = resp.get('nextPageToken')

        if pageToken is None:
            break

def analyse(auth_code):
    gmail = build_service(auth_code)

    MAX_COUNT = 10

    i = 0

    for msg in get_all_messages(gmail): 
        if i > MAX_COUNT: break

        m = gmail.users().messages().get(id=msg['id'], userId='me', format='raw').execute()
        msg_str = base64.urlsafe_b64decode(m['raw'].encode('ASCII'))
        mime_msg = email.message_from_string(msg_str.decode())
        messageMainType = mime_msg.get_content_maintype()
        
        import json

        if messageMainType == 'multipart':
            for part in mime_msg.get_payload():
                if part.get_content_maintype() == 'text':
                    print(json.dumps(part.get_payload()))
            
        elif messageMainType == 'text':
            print(json.dumps(mime_msg.get_payload()))

        i += 1

    return AnalyseResult()

