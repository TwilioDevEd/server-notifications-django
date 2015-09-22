from twilio.rest import TwilioRestClient
from django.core.exceptions import MiddlewareNotUsed
import os
import logging

logger = logging.getLogger(__name__)

MESSAGE = """[This is a test] ALERT!
It appears the server is having issues.
Exception: %s.
Go to: http://newrelic.com for more details."""

NOT_CONFIGURED_MESSAGE = """Cannot initialize Twilio notification
middleware. Required enviroment variables TWILIO_ACCOUNT_SID, or
TWILIO_AUTH_TOKEN or TWILIO_NUMBER missing"""


class TwilioNotificationsMiddleware(object):

    def __init__(self):
        (twilio_number, twilio_client) = self._twilio_config()

        self.twilio_number = twilio_number
        self.twilio_client = twilio_client
        self.administrators = self._administrators()

    def _twilio_config(self):
        twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_number = os.environ.get('TWILIO_NUMBER')

        if not all([twilio_account_sid,
                    twilio_auth_token,
                    self.twilio_number]):

            logger.error(NOT_CONFIGURED_MESSAGE)
            raise MiddlewareNotUsed

        return (twilio_number,
                TwilioRestClient(twilio_account_sid, twilio_auth_token))

    def _send_message(self, body, to):
        self.twilio_client.messages.create(body=body, to=to,
                                           from_=self.twilio_number)

    def _administrators(self):
        # Read administrators
        pass

    def process_exception(self, request, exception):
        exception_message = str(exception)
        message_to_send = MESSAGE % exception_message

        for admin in self.administrators:
            self._send_message(message_to_send, admin.phone_number)

        return None
