# settings/local.py
from .base import *

import json
# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured
# JSON-based secrets module
with open(os.path.join(BASE_DIR, "project1_local_config.json")) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
ENGINE = get_secret("ENGINE")
NAME = get_secret("NAME")
USER = get_secret("USER")
PASSWORD = get_secret("PASSWORD")
HOST = get_secret("HOST")
PORT = get_secret("PORT")

SECRET_KEY = SECRET_KEY

DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
    }
}
