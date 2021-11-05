# Server Notifications with Twilio and Django

[![Build and test](https://github.com/TwilioDevEd/server-notifications-django/actions/workflows/build_test.yml/badge.svg)](https://github.com/TwilioDevEd/server-notifications-django/actions/workflows/build_test.yml)
[![Coverage Status](https://coveralls.io/repos/TwilioDevEd/server-notifications-django/badge.svg?branch=master&service=github)](https://coveralls.io/github/TwilioDevEd/server-notifications-django?branch=master)

Use Twilio to send SMS alerts so that you never miss a critical issue.

[Read the full tutorial here](https://www.twilio.com/docs/tutorials/walkthrough/server-notifications/python/django)!

## Quickstart

This project is built using the [Django](https://www.djangoproject.com/) web framework. It runs on Python 3.6+.

To run the app locally, first clone this repository and `cd` into its directory. Then:

1. Create a new virtual environment:
    - If using vanilla with Python 3 [virtualenv](https://docs.python.org/3/library/venv.html):

        ```
        python -m venv venv
        source venv/bin/activate
        ```

    - If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

        ```
        mkvirtualenv server-notifications-django
        ```

1. Install the requirements:

    ```
    pip install -r requirements.txt
    ```

1. Copy the `.env.example` file to `.env`, and edit it to include your Twilio API credentials (found at https://www.twilio.com/user/account/voice)
1. For the TWILIO_NUMBER variable you'll need to provision a new number in the [Manage Numbers page](https://www.twilio.com/user/account/phone-numbers/incoming) under your account. The phone number should be in E.164 format
1. (Optional) This project integrate [python-dotenv](https://github.com/theskumar/python-dotenv) to automatically load the `.env` file. Alternatively, you can run `source .env` to apply the environment variables (or even use [autoenv](https://github.com/kennethreitz/autoenv))
1. Customize `config/administrators.json` with your phone number.
1. Start the development server

    ```
    python manage.py runserver
    ```
1. Go to [http://localhost:8000/error](http://localhost:8000/error/). You'll receive a text shortly with details on the exception.

### Use Production Environment

Follow previous guide and in step 3 do:

1. Copy the `.env.production.example` file to `.env`, and edit it to include your Twilio API credentials (found at https://www.twilio.com/user/account/voice) and add the `DJANGO_SECRET_KEY`

## Run the tests

You can run the tests locally through [coverage](http://coverage.readthedocs.org/):

```
$ coverage run manage.py test --settings=twilio_sample_project.settings.test
```

You can then view the results with `coverage report` or build an HTML report with `coverage html`.
