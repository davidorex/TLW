from .base import *
import os

print("=" * 50)
print("LOADING DEVELOPMENT SETTINGS!")

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Load the secret key from an environment variable
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-dev-secret-key')

print(f"DEBUG is now: {DEBUG}")
print(f"ALLOWED_HOSTS are now: {ALLOWED_HOSTS}")
print(f"SECRET_KEY is set to: {SECRET_KEY}")
print("=" * 50)
