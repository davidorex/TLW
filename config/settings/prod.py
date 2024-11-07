# prod.py
from .base import *

print("="*50)
print("LOADING PRODUCTION SETTINGS!")
print(f"DEBUG is being set to: {DEBUG}")
print(f"ALLOWED_HOSTS will be: {ALLOWED_HOSTS}")
print("="*50)

DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')