"""
WSGI config for the project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use our production settings as our default settings, which is most secure
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "twilio_sample_project.settings.production")

# Get a WSGI application for our project
application = get_wsgi_application()
