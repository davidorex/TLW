# Django Configuration Structure

### Directory Layout
```
config/
├── __init__.py
├── settings/
│   ├── __init__.py
│   ├── base.py
│   ├── dev.py
│   └── prod.py
```

### Base Settings (base.py)
```python
Purpose: Core settings shared across all environments

Required Elements:
- Path Configuration
    BASE_DIR = defined from settings location
    PROJECT_ROOT = absolute path to project

- Security
    SECRET_KEY = from env
    ALLOWED_HOSTS = []
    AUTH_USER_MODEL = 'users.User'
    AUTH_PASSWORD_VALIDATORS = [...] 

- Application Definition
    DJANGO_APPS = [
        'django.contrib.admin',
        ...
    ]
    
    THIRD_PARTY_APPS = [
        'simple_history',
        'safedelete',
        ...
    ]
    
    LOCAL_APPS = [
        'core.apps.CoreConfig',
        'calendar.apps.CalendarConfig',
        ...
    ]
    
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

- Middleware Configuration
    Including:
    - Security
    - Sessions
    - Common
    - CSRF
    - Auth
    - Messages
    - Security Headers

- Database Configuration
    DATABASES = {
        'default': {
            'ENGINE': from env,
            ...
        }
    }

- Cache Framework
    CACHES = {
        'default': {
            'BACKEND': from env,
            ...
        }
    }

- Templates/Static/Media
    TEMPLATES = [...]
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

- Internationalization
    TIME_ZONE = 'UTC'
    USE_TZ = True
    etc.

- Logging Configuration
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {...},
        'handlers': {...},
        'loggers': {...}
    }
```

### Development Settings (dev.py)
```python
Purpose: Local development configuration

from .base import *

Elements to Override:
- Debug Settings
    DEBUG = True
    TEMPLATES[0]['OPTIONS']['debug'] = True

- Security
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    INTERNAL_IPS = ['127.0.0.1']

- Development Apps
    INSTALLED_APPS += [
        'debug_toolbar',
        'django_extensions',
    ]

- Development Middleware
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

- File Storage
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_ROOT = BASE_DIR / 'media'

- Email Backend
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

- Development-specific Logging
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
    }
```

### Production Settings (prod.py)
```python
Purpose: Production environment configuration

from .base import *

Elements to Override:
- Security Settings
    DEBUG = False
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

- Hosts/CORS
    ALLOWED_HOSTS = ['.example.com']  # from env
    CORS_ORIGIN_WHITELIST = [...]  # from env

- Cache Configuration
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': from env,
        }
    }

- Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': from env,
            ...
        }
    }

- Static/Media Files
    STATIC_ROOT = '/var/www/static/'
    MEDIA_ROOT = '/var/www/media/'
    
    # Optional: CDN configuration
    AWS_S3_CUSTOM_DOMAIN = from env
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

- Email Configuration
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = from env
    etc.

- Logging
    LOGGING = production_logging_config
```

### Environment Variables (.env)
```python
Required Variables:
# Base
DJANGO_SETTINGS_MODULE=config.settings.prod
DJANGO_SECRET_KEY=

# Database
DATABASE_URL=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

# Cache
REDIS_URL=

# Email
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# AWS/Storage
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# Security
ALLOWED_HOSTS=
CORS_ORIGINS=
```

### Usage Instructions
```python
# Development
export DJANGO_SETTINGS_MODULE=config.settings.dev
python manage.py runserver

# Production
export DJANGO_SETTINGS_MODULE=config.settings.prod
gunicorn config.wsgi:application
```

Want me to elaborate on any section or add additional configurations?