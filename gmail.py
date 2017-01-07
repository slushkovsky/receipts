import os

from apiclient import discovery
import httplib2
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build


PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
CLIENT_SECRET_FILE = os.path.join(PROJECT_DIR, 'client_secret.json')
REQUIRED_SCOPES =[
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

def parse(auth_code):
#    credentials = client.credentials_from_clientsecrets_and_code(CLIENT_SECRET_FILE, REQUIRED_SCOPES, auth_code)


    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, ' '.join(REQUIRED_SCOPES)) 	
    flow.redirect_uri = 'http://a-c-b.tech/google_access'

    try:
        credentials = flow.step2_exchange(auth_code)
        print('Success')
    except FlowExchangeError as error:
    	print('An error occurred: {}'.format(error))

    gmail = build(
        serviceName='gmail', 
        version='v1',
        http=credentials.authorize(httplib2.Http())
    )

    resp = gmail.users().messages().list(userId='me').execute()

    print(resp)
#    http_auth = credentials.authorize(httplib2.Http())
#    service = discovery.build('gmail', 'v1', http=http_auth)

 #   response = service.users().messages().list(userId='me').execute()

  #  print(response)
    
