# sends message

import base64
import httplib2
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
from email.message import EmailMessage

# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'credentials.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = ['https://www.googleapis.com/auth/gmail.compose',
               'https://www.googleapis.com/auth/gmail.labels',
               'https://mail.google.com/'
               ]

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
# This is where it fails.
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)

message = EmailMessage()
message.set_content('This is automated mail to be sent to 4 people')

message['To'] = 'userashrivastava@gmail.com'
message['From'] = 'ayushi.s@grexit.com'
message['Subject'] = 'Training Exercise'

# encoded message
encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

create_message = {
    'raw': encoded_message,
    # 'labelIds': ['Training Exercise']
}

# create and send it
try:
    list = gmail_service.users().labels().list(userId="me").execute()
    result = list.get('labels', [])
    # print(result)

    i = 0
    create = False
    while i < len(result):
        if(result[i]['name'] != 'Training Exercise'):
            i += 1
        else:
            create = True
            break

    if(create == False):
        label = gmail_service.users().labels().create(
            userId="me", body={
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show",
                "name": "Training Exercise",
                # "id": "Training_Exercise"
            }).execute()

    message = (gmail_service.users().messages().send(
        userId="me", body=create_message).execute())
    print('Message Id: %s' % message['id'])
    print(message)

    # result = (gmail_service.users().messages().modify(
    #     userId='me',
    #     id=message['id'],  # extracts the sent message id
    #     # sets which labels to add
    #     body={"addLabelIds": ["TRAINING EXERCISE"]},
    # )).execute()
    # print(result)


except Exception as error:
    print('An error occurred: %s' % error)
