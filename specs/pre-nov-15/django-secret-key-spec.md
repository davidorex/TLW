# Django Secret Key Management

### Directory Layout
```
config/
├── settings/
│   ├── __init__.py
│   ├── base.py
│   ├── dev.py
│   ├── prod.py
│   └── utils.py    # Key generation utilities
```

### Key Generation Utility (utils.py)
```python
Purpose: Safe secret key generation and management

from django.core.management.utils import get_random_secret_key
from pathlib import Path
import os

def generate_secret_key(env_type):
    """
    Generates and stores secret key for specified environment.
    
    Usage:
    - Dev: Stores in .env.dev
    - Prod: Must be set in production env vars
    """
    
    if env_type == 'dev':
        env_file = Path('.env.dev')
        if not env_file.exists():
            key = get_random_secret_key()
            env_file.write_text(f"DJANGO_SECRET_KEY={key}\n")
            return key
        return None
    
    elif env_type == 'prod':
        # Only generate for display, never store
        return get_random_secret_key()
```

### Development Settings (dev.py)
```python
from .utils import generate_secret_key

# Generate dev key if not exists
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    generate_secret_key('dev')
)

if not SECRET_KEY:
    raise ValueError(
        "Secret key not found. Delete .env.dev to generate new one."
    )
```

### Production Settings (prod.py)
```python
# Strict production key requirement
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    raise ValueError(
        "Production secret key must be set in environment variables."
        "\nGenerate with: python manage.py generate_secret_key"
    )
```

### Management Command
```python
# management/commands/generate_secret_key.py

class Command(BaseCommand):
    help = 'Generates a new secret key for specified environment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--env',
            choices=['dev', 'prod'],
            default='prod',
            help='Environment to generate key for'
        )

    def handle(self, *args, **options):
        from ...settings.utils import generate_secret_key
        
        key = generate_secret_key(options['env'])
        
        if options['env'] == 'prod':
            self.stdout.write(
                "Add this to production environment:\n"
                f"DJANGO_SECRET_KEY={key}"
            )
        else:
            self.stdout.write(
                "Development key stored in .env.dev"
            )
```

### Usage
```bash
# Development
# Automatic on first run, or:
python manage.py generate_secret_key --env dev

# Production
python manage.py generate_secret_key --env prod
# Copy output to production environment variables
```

### Security Notes:
```
1. Development:
   - Key stored in .env.dev
   - .env.dev in .gitignore
   - Auto-generated if missing

2. Production:
   - Never store key in files
   - Generate and set in env vars
   - Rotate periodically
   - Min 50 characters
   - Use secure environment variable handling
```

Want me to detail any part further?