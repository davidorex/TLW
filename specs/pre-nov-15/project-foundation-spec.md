# Foundation Requirements

```
### Directory Layout -- do not create directories that already exist. create directories only if they do not already exist. If files exist in the directories, do not overwrite or delete existing content in them. If existing content needs to be edited to bring in line with spec, get explicity confirmation from user. if content in files already meets spec requirements, report that spec is satisfied for that element.
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
├── schoolcalendar/             # Calendar app
│   ├── models/
│   ├── views/
│   ├── api/
│   └── templates/
├── static/
├── templates/
├── requirements.py
├── manage.py
```

### Core App Registration -- Confirm the following lines exist in config/settings/base.py -- if they do not exist, add the line while deleting nothing.
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
    'schoolcalendar.apps.CalendarConfig',
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