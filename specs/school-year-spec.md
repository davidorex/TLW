# SchoolYear Model Specification

### Base Configuration
```python
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

Requirements:
- django-simple-history
- django-model-utils
- django-safedelete
```

### Model Structure
```python
class CalendarBaseModel(SafeDeleteModel, TimeStampedModel):
    """
    Abstract base class for all calendar models.
    Provides: Soft delete, timestamps, history, metadata
    """
    id = UUIDField(primary_key=True)
    is_active = BooleanField(default=True)
    metadata = JSONField(default=dict, validators=[validate_metadata_schema])
    created_by = ForeignKey(settings.AUTH_USER_MODEL)
    modified_by = ForeignKey(settings.AUTH_USER_MODEL)
    history = HistoricalRecords()

    class Meta:
        abstract = True
```

### SchoolYear Fields Detail
```python
TERM_CHOICES = [
    ('SEMESTER', _('Semester with Quarters')),
    ('TRIMESTER', _('Trimester'))
]

academic_year = CharField(
    max_length=9,
    validators=[
        RegexValidator(
            regex=r'^\d{4}-\d{4}$',
            message='Format must be YYYY-YYYY'
        )
    ],
    unique=True,
    help_text=_('Academic year in YYYY-YYYY format')
)

metadata = JSONField(
    default=dict,
    validators=[validate_calendar_metadata],
    help_text=_('Schema: {
        "holiday_dates": ["YYYY-MM-DD", ...],
        "term_breaks": [
            {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
            ...
        ],
        "config": {
            "week_start": 0-6,
            "default_template": "uuid",
            ...
        }
    }')
)

# Additional fields as specified above...
```

### Required Custom Methods
```python
def generate_terms(self):
    """
    Creates Term objects based on term_structure.
    Called: post_save if terms don't exist
    
    For SEMESTER:
    - Creates 2 terms
    - Each term gets 2 quarters
    - Considers term_breaks from metadata

    For TRIMESTER:
    - Creates 3 equal terms
    - Considers term_breaks from metadata
    """

def get_current_term(self, date=None):
    """
    Returns active term for date (defaults to today).
    Uses caching with date-based key.
    """

def is_valid_date(self, check_date):
    """
    Validates if date is:
    - Within year bounds
    - Not in holiday_dates
    - Not in term_breaks
    Returns: bool
    """
```

### Required Managers
```python
class SchoolYearManager(models.Manager):
    def current(self):
        """Returns year containing today's date"""
        
class ActiveManager(models.Manager):
    def get_queryset(self):
        """Filters is_active=True"""
```

### Caching Implementation
```python
CACHE_KEYS = {
    'current_term': 'school_year:{id}:current_term:{date}',
    'term_boundaries': 'school_year:{id}:terms'
}

# Cache invalidation required in:
- save()
- metadata updates
- term changes
```

### Signal Handlers Required
```python
@receiver(post_save, sender=SchoolYear)
def create_terms(sender, instance, created, **kwargs):
    """Generates terms if needed"""

@receiver(pre_save, sender=SchoolYear)
def validate_metadata(sender, instance, **kwargs):
    """Validates metadata schema"""
```

### Test Cases Detail
```python
def test_year_validation():
    """
    1. Create with valid dates
    2. Create with invalid year format
    3. Create with end_date < start_date
    4. Create with invalid metadata
    """

def test_term_generation():
    """
    1. Verify semester creates 2 terms, 4 quarters
    2. Verify trimester creates 3 terms
    3. Verify term dates don't overlap
    4. Verify breaks are respected
    """

# Additional test cases as specified above...
```

Implementation Requirements:
1. Use Django's built-in validation
2. Implement proper caching strategy
3. Follow Django's database optimization guidelines
4. Add comprehensive documentation
5. Include all translations
6. Follow Django security best practices

Want me to continue with the Term model specification?
