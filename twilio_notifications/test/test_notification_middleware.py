from __future__ import unicode_literals
import unittest
from mock import patch, Mock

from twilio_notifications.middleware import TwilioNotificationsMiddleware
from twilio_notifications.middleware import MessageClient
from twilio_notifications.middleware import MESSAGE


class TestNotificationMiddleware(unittest.TestCase):
    @patch('twilio_notifications.middleware.load_admins_file')
    @patch('twilio_notifications.middleware.load_twilio_config')
    def test_notify_on_exception(self, mock_load_admins_file, mock_load_twilio_config):
        admin_number = '+15550005555'
        sending_number = '+15555550000'

        mock_load_admins_file.return_value = [
            {'name': 'Some name', 'phone_number': admin_number}
        ]

        mock_client = Mock(spec=MessageClient)
        mock_load_twilio_config.return_value = (sending_number, mock_client)

        middleware = TwilioNotificationsMiddleware()
        exception_message = 'Some exception message'

        middleware.process_exception(None, 'Some exception message')

        mock_client.send_message.assert_called_once_with(
            MESSAGE % exception_message, admin_number
        )
