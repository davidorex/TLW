# School Calendar App Specification - Core Structure & Implementation
Version: 2.0 (2024-02-09 14:55 UTC)
Status: CONTROLLING
Component: Core App Structure and Installation

### Implementation Sequence
```bash
# 1. Installation
pip install -r requirements/base.txt

# 2. App Registration
# config/settings/base.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'core.apps.CoreConfig',  # Must be before schoolcalendar
    'schoolcalendar.apps.SchoolCalendarConfig',
]

# 3. Database Setup
python manage.py makemigrations schoolcalendar
python manage.py migrate schoolcalendar

# 4. Verification
python manage.py test schoolcalendar
```

### Directory Structure
```
schoolcalendar/
├── __init__.py
├── apps.py          
├── models/          
│   ├── __init__.py  
│   ├── school_year.py
│   ├── term.py
│   ├── quarter.py
│   ├── period_template.py
│   └── period_content.py
├── tests/           
│   ├── __init__.py
│   ├── factories.py
│   └── test_models.py
├── templatetags/
│   ├── __init__.py
│   └── schoolcalendar_tags.py
├── templates/
│   └── schoolcalendar/
│       ├── base/
│       ├── components/
│       └── views/
├── admin/
│   ├── __init__.py
│   └── site.py
└── migrations/
```

### Admin Registration
```python
# schoolcalendar/admin/__init__.py
from django.contrib import admin
from ..models import (
    SchoolYear, Term, Quarter,
    PeriodTemplate, PeriodContent
)

admin.site.register(SchoolYear)
admin.site.register(Term)
admin.site.register(Quarter)
admin.site.register(PeriodTemplate)
admin.site.register(PeriodContent)

# Custom admin site configuration
admin.site.site_header = 'School Calendar Administration'
admin.site.site_title = 'School Calendar'
admin.site.index_title = 'Calendar Management'
```

### App Configuration
```python
# schoolcalendar/apps.py

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SchoolCalendarConfig(AppConfig):
    name = 'schoolcalendar'
    verbose_name = _('School Calendar')
    
    def ready(self):
        import schoolcalendar.signals
        from core.registry import ContentRegistry
        from . import models
        ContentRegistry.register_calendar_models()
        self.setup_cache_config()

    def setup_cache_config(self):
        from django.core.cache import cache
        cache.set_many({
            'CALENDAR_CACHE_VERSION': '2.0',
            'CALENDAR_CACHE_TIMEOUT': 3600,
        })
```

### Required Dependencies
```python
# requirements/base.txt additions
django>=4.2,<5.0
django-model-utils>=4.3.1
django-simple-history>=3.4.0
```

### Models Registration
```python
# schoolcalendar/models/__init__.py

from .school_year import SchoolYear
from .term import Term
from .quarter import Quarter
from .period_template import PeriodTemplate
from .period_content import PeriodContent

__all__ = [
    'SchoolYear',
    'Term',
    'Quarter',
    'PeriodTemplate',
    'PeriodContent',
]
```

### URL Configuration
```python
# config/urls.py
urlpatterns = [
    path('calendar/', include('schoolcalendar.urls')),
]

# schoolcalendar/urls.py
from django.urls import path
from . import views

app_name = 'schoolcalendar'

urlpatterns = [
    path('', views.CalendarView.as_view(), name='index'),
]
```

### Integration Settings
```python
# config/settings/base.py
SCHOOLCALENDAR_SETTINGS = {
    'content_types': [
        'course.Unit',
        'course.Lesson',
        'assessment.Task',
        'study.Resource'
    ],
    'role_views': [
        'student',
        'teacher',
        'admin'
    ],
    'display_modes': [
        'schedule',
        'standalone'
    ]
}
```

---End Part 1---