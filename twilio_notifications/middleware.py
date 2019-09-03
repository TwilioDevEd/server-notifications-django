import json
import logging
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
from twilio.rest import Client

logger = logging.getLogger(__name__)

dotenv_path = settings.PROJECT_PATH / '.env'
logger.debug(f'Reading .env file at: {dotenv_path}')
load_dotenv(dotenv_path=dotenv_path)


MESSAGE = """[This is a test] ALERT! It appears the server is having issues.
Exception: {0}"""

NOT_CONFIGURED_MESSAGE = (
    "Required enviroment variables "
    "TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing."
)


def load_admins_file():
    admins_json_path = settings.PROJECT_PATH / 'config' / 'administrators.json'
    logger.debug(f'Loading administrators info from: {admins_json_path}')
    return json.loads(admins_json_path.read_text())


def load_twilio_config():
    logger.debug('Loading Twilio configuration')

    twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_number = os.getenv('TWILIO_NUMBER')

    if not all([twilio_account_sid, twilio_auth_token, twilio_number]):
        raise ImproperlyConfigured(NOT_CONFIGURED_MESSAGE)

    return (twilio_number, twilio_account_sid, twilio_auth_token)


class MessageClient:
    def __init__(self):
        logger.debug('Initializing messaging client')

        (
            twilio_number,
            twilio_account_sid,
            twilio_auth_token,
        ) = load_twilio_config()

        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)

        logger.debug('Twilio client initialized')

    def send_message(self, body, to):
        self.twilio_client.messages.create(
            body=body,
            to=to,
            from_=self.twilio_number,
            # media_url=['https://demo.twilio.com/owl.png']
        )


class TwilioNotificationsMiddleware:
    def __init__(self, get_response):
        logger.debug('Initializing Twilio notifications middleware')

        self.administrators = load_admins_file()
        self.client = MessageClient()
        self.get_response = get_response

        logger.debug('Twilio notifications middleware initialized')

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        message_to_send = MESSAGE.format(exception)

        for admin in self.administrators:
            self.client.send_message(message_to_send, admin['phone_number'])

        logger.info('Administrators notified!')
        return None
