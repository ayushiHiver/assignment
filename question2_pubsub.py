# import the required libraries
from ast import Not
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import base64
import email
from bs4 import BeautifulSoup
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools
import httplib2
from email.message import EmailMessage

userIdsSet = {"userbshrivastava@gmail.com",
              "usercshrivastava@gmail.com", "userdshrivastava@gmail.com"}

# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'my_creds.json'
MY_TOPIC_NAME = 'projects/pubsub-project-359009/topics/publish-topic-gmail'
# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = ['https://www.googleapis.com/auth/gmail.compose',
               'https://www.googleapis.com/auth/gmail.labels',
               'https://mail.google.com/',
               'https://www.googleapis.com/auth/gmail.readonly'
               ]


def getEmails():

    savedHistoryId = None
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
    service = build('gmail', 'v1', http=http)

    request = {'labelIds': ['Label_1'],
               'topicName': MY_TOPIC_NAME}

    something = service.users().stop(userId='me').execute()
    something = service.users().watch(userId='me', body=request).execute()
    print(something)

    if os.path.exists('history.txt'):
        with open('history.txt', 'rb') as file:
            savedHistoryId = file.read()
            print(savedHistoryId)

# {
#   "startHistoryId": old_history_Id,
#   "userId": 'me',
#   "labelId": ["UNREAD"],
#   "historyTypes": ["messageAdded","labelAdded"]
# }
    if savedHistoryId is not None:
        some = service.users().history().list(
            userId='me', startHistoryId=str(savedHistoryId, 'UTF-8'),
            historyTypes=["messageAdded", "labelAdded"]).execute()
        print(some)

        s = set()
        for x in some['history']:
            if "messagesAdded" in x:
                for y in x['messagesAdded']:
                    s.add(y['message']['id'])
            for y in x['messages']:
                s.add(y['id'])
        print(s)

        # savedHistoryId = some['historyId']
        with open('history.txt', 'wb') as file:
            file.write(bytes(str(something['historyId']), 'utf-8'))

    if savedHistoryId is None:
        with open('history.txt', 'wb') as file:
            file.write(bytes(str(something['historyId']), 'utf-8'))

    with open('history.txt', 'rb') as file:
        savedHistoryId = file.read()

    decoded_data = None
    for msgId in s:
        txt = service.users().messages().get(
            userId='me', id=msgId).execute()
        print("txt", txt)
        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']
            # print(headers)
            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)
            # print(decoded_data)
            # Now, the data obtained is in lxml. So, we will parse
            # it with BeautifulSoup library
            # soup = BeautifulSoup(decoded_data, "lxml")
            # body = soup.body()

            # Printing the subject, sender's email and message
            print("Subject: ", subject)
            print("From: ", sender)
            # print("Message: ", body)
            print('\n')
        except:
            pass

        for x in userIdsSet:
            message = EmailMessage()
            message.set_content(
                'This is reply to E1')
            message['To'] = "me"
            message['From'] = 'userbshrivastava@gmail.com'
            message['Subject'] = 'Training Exercise'

            # encoded message
            encoded_message = base64.urlsafe_b64encode(
                message.as_bytes()).decode()
            insert = (service.users().messages().insert(
                userId="me",
                body={
                    "historyId": str(savedHistoryId, 'UTF-8'),
                    "id": "E1email",
                    "labelIds": ["INBOX", "Label_1"],
                    "payload": {
                        "body": {
                            "data": decoded_data
                        },
                        "headers": [
                            {
                                "name": "To",
                                "value": "me"
                            },
                            {
                                "name": "From",
                                "value": "userashrivastava@gmail.com"
                            }
                        ]
                    },
                    "raw": encoded_message,
                    "threadId": txt['threadId']
                })).execute()
            print("insert", insert)

    something = service.users().stop(userId='me').execute()
    print(something)


getEmails()
