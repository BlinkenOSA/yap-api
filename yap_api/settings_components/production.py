# SECURITY WARNING: keep the secret key used in production secret!
import os
from yap_api.settings import BASE_DIR

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public')

MEDIA_URL = '/reports/'

CORS_ORIGIN_ALLOW_ALL = True
