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
CLIENT_SECRET_FILE = 'creds_b.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = ['https://www.googleapis.com/auth/gmail.compose',
               'https://www.googleapis.com/auth/gmail.labels',
               #    'https://www.googleapis.com/auth/gmail.metadata',
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
message.set_content('This is reply to E1')

message['To'] = 'userashrivastava@gmail.com'
message['From'] = 'userbshrivastava@gmail.com'
message['Subject'] = 'Training Exercise'

# encoded message
encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

# find the thread and message with given label
old_message = gmail_service.users().messages().list(
    userId="me", labelIds=["INBOX"], q="label:Training Exercise").execute()
print(old_message)
print(old_message['messages'][0]['id'])
print(old_message['messages'][0]['threadId'])

message['In-Reply-To'] = old_message['messages'][0]['id']
message['References'] = old_message['messages'][0]['id']
create_message = {
    'threadId': old_message['messages'][0]['threadId'],
    'raw': encoded_message,
    # 'historyId': threads['threads'][0]['historyId'],
}

message = (gmail_service.users().messages().send(
    userId="me", body=create_message).execute())
print('Message Id: %s' % message['id'])
print(message)
