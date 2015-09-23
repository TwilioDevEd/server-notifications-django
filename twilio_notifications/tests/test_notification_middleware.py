from __future__ import unicode_literals
from mock import patch, Mock
from django.core.exceptions import MiddlewareNotUsed
import unittest
import os

from twilio_notifications.middleware import TwilioNotificationsMiddleware
from twilio_notifications.middleware import MessageClient, load_twilio_config
from twilio_notifications.middleware import MESSAGE


class TestNotificationMiddleware(unittest.TestCase):

    @patch('twilio_notifications.middleware.load_twilio_config')
    @patch('twilio_notifications.middleware.load_admins_file')
    def test_notify_on_exception(self, mock_load_admins_file,
                                 mock_load_twilio_config):

        # Given
        admin_number = '+15550005555'
        sending_number = '+1555555000'

        mock_load_admins_file.return_value = [
            {'name': 'Some name', 'phone_number': admin_number}
        ]

        mock_message_client = Mock(spec=MessageClient)
        mock_load_twilio_config.return_value = (sending_number,
                                                '4ccou1s1d', 'som3tok3n')

        middleware = TwilioNotificationsMiddleware()
        middleware.client = mock_message_client

        exception_message = 'Some exception message'

        # When
        middleware.process_exception(None, 'Some exception message')

        # Then
        mock_message_client.send_message.assert_called_once_with(
            MESSAGE % exception_message, admin_number
        )

    def test_correct_load_twilio_config(self):
        os.environ['TWILIO_ACCOUNT_SID'] = 'some4acc0un1s1d'
        os.environ['TWILIO_AUTH_TOKEN'] = 'sometok3n'
        os.environ['TWILIO_NUMBER'] = '322937498'

        try:
            load_twilio_config()
        except MiddlewareNotUsed:
            self.fail('MiddlewareNotUsed when correctly configured')

    def test_fail_load_twilio_config(self):
        os.environ['TWILIO_ACCOUNT_SID'] = 'some4acc0un1s1d'
        os.environ['TWILIO_AUTH_TOKEN'] = 'sometok3n'
        os.environ.pop('TWILIO_NUMBER')

        with self.assertRaises(MiddlewareNotUsed):
            load_twilio_config()
