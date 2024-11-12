from .base import *
import os

print("=" * 50)
print("HEY! LOADING DEVELOPMENT SETTINGS!")

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Load the secret key from an environment variable
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'nazewb@jxtz53zhtn_#ydnwo7z50wrtd=$vdrh+e24^v+nv3(%')

# Development static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

print(f"DEBUG is now: {DEBUG}")
print(f"ALLOWED_HOSTS are now: {ALLOWED_HOSTS}")
print(f"SECRET_KEY is set to: {SECRET_KEY}")
print("=" * 50)
