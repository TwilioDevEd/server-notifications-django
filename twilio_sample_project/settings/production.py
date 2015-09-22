'''
Production settings

- Set secret key from environment variable
'''

from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Allow all hosts, so we can run on PaaS's like Heroku
ALLOWED_HOSTS = ['*']
