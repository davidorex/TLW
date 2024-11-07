# Foundation Requirements

### requirements.txt
```
# Core
Django>=4.2,<5.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9.9

# Models/DB
django-model-utils>=4.3.1
django-simple-history>=3.4.0
django-safedelete>=1.3.1
django-fsm>=2.8.1

# API/Forms
djangorestframework>=3.14.0
django-filter>=23.5
django-crispy-forms>=2.0

# Security/Auth
django-allauth>=0.57.0
django-permissions-policy>=4.18.0

# Cache/Performance
redis>=5.0.1
django-redis>=5.4.0

# Development
django-debug-toolbar>=4.2.0
django-extensions>=3.2.3
pytest-django>=4.7.0
factory-boy>=3.3.0
```

### .gitignore
```
# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon
._*
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent

# Python
*.py[cod]
__pycache__/
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment
.env
.env.*
!.env.example
.venv
venv/
ENV/

# IDE - VS Code
.vscode/
*.code-workspace

# IDE - PyCharm
.idea/
*.iml
*.iws
.idea_modules/

# Coverage/Tests
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
```

### Directory Layout
```
project_root/
├── config/               # Project configuration
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
├── core/                 # Core functionality
│   ├── management/
│   ├── models/
│   │   ├── abstracts.py
│   │   └── mixins.py
│   ├── utils/
│   └── views/
├── calendar/             # Calendar app
│   ├── models/
│   ├── views/
│   ├── api/
│   └── templates/
├── static/
├── templates/
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── manage.py
├── pytest.ini
├── .env.example
└── README.md
```

### Core App Registration
```python
# config/settings/base.py

INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'simple_history',
    'django_filters',
    'crispy_forms',
    'allauth',
    
    # Local apps
    'core.apps.CoreConfig',  # Must be loaded first
    'calendar.apps.CalendarConfig',
    # Other local apps...
]

# core/apps.py
class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Core'

    def ready(self):
        import core.signals  # Register signals
        self.register_app_settings()
```

### Common Patterns

```python
# core/models/mixins.py

class TimestampMixin(models.Model):
    """Adds created/modified timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserStampMixin(models.Model):
    """Adds user tracking"""
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_created"
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_modified"
    )

    class Meta:
        abstract = True

# core/views/mixins.py

class PermissionRequiredMixin:
    """Base permission handling"""
    permission_required = None

    def has_permission(self):
        if self.permission_required is None:
            return True
        return self.request.user.has_perm(self.permission_required)

class AuditableMixin:
    """Tracks model changes"""
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
```

### Integration Points
```python
# core/registry.py

class ContentRegistry:
    """
    Registers content types that can be scheduled in periods.
    Provides interface for content injection.
    """
    _registry = {}

    @classmethod
    def register(cls, model_class, **options):
        """Register a model for period scheduling"""
        cls._registry[model_class] = options

    @classmethod
    def get_content_types(cls):
        """Return all registered content types"""
        return cls._registry.keys()

# Example Usage in calendar/models.py
from core.registry import ContentRegistry

@ContentRegistry.register
class ClassSession(models.Model):
    """Can be scheduled in periods"""
    def get_period_content(self):
        """Return formatted content for period"""
        return {
            'title': self.name,
            'type': 'CLASS',
            'metadata': {...}
        }

# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save)
def handle_content_changes(sender, instance, **kwargs):
    """
    Generic signal handler for content changes.
    Updates period content when source changes.
    """
    if sender in ContentRegistry.get_content_types():
        # Update related period content
        pass
```

This provides:
1. Complete environment setup
2. Project structure
3. Common utilities/patterns
4. Integration framework

Want me to detail any section further?