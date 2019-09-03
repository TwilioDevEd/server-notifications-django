import unittest
from .urls import error_handler


class TestTwilioSampleProject(unittest.TestCase):
    def test_error_handler(self):
        self.assertRaises(Exception, error_handler, None)
