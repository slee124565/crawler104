from __future__ import print_function
import fire
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import logging
FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)
TOKEN_STORAGE_FILE = 'token.json'
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def create_token_storage_file():
    logger.info('create_token_storage_file {}'.format(TOKEN_STORAGE_FILE))
    store = file.Storage(TOKEN_STORAGE_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
        logger.info('credential created')
    return creds


class Crawler104(object):
    user_id = None
    creds = None

    def __init__(self, user_id='lee.shiueh@gmail.com'):
        # store = file.Storage(TOKEN_STORAGE_FILE)
        # self.creds = store.get()
        # if not self.creds or self.creds.invalid:
        #     flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        #     self.creds = tools.run_flow(flow, store)
        self.user_id = user_id
        self.creds = create_token_storage_file()

    @staticmethod
    def rm_token_storage_file():
        if os.path.exists(TOKEN_STORAGE_FILE):
            logger.info('remove token storage file {}'.format(TOKEN_STORAGE_FILE))
            os.remove(TOKEN_STORAGE_FILE)
        else:
            logger.info('file {} not exist'.format(TOKEN_STORAGE_FILE))

    @property
    def gmail(self):
        return build('gmail', 'v1', http=self.creds.authorize(Http()))

    def gmail_labels(self):
        results = self.gmail.users().labels().list(userId=self.user_id).execute()
        labels = results.get('labels', [])
        return labels

    def get_gmail_messages(self):
        pass


if __name__ == '__main__':
    if not os.path.exists(TOKEN_STORAGE_FILE):
        create_token_storage_file()
    else:
        logger.info('token.json file exist')

    fire.Fire(Crawler104)
