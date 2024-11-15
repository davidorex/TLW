# SchoolYear Model Specification

### Base Configuration
```python
from core.models.abstracts import MetadataModel
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

Location: calendar/models/academic_year.py
```

### Model Definition
```python
class SchoolYear(MetadataModel):
    """
    Defines academic year structure and boundaries.
    Controls term generation and provides calendar validation.
    """

    TERM_CHOICES = [
        ('SEMESTER', _('Semester with Quarters')),
        ('TRIMESTER', _('Trimester'))
    ]

    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "holiday_dates": {
                "type": "array",
                "items": {"type": "string", "format": "date"}
            },
            "term_breaks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "start": {"type": "string", "format": "date"},
                        "end": {"type": "string", "format": "date"},
                        "description": {"type": "string"}
                    },
                    "required": ["start", "end"]
                }
            },
            "config": {
                "type": "object",
                "properties": {
                    "week_start": {"type": "integer", "minimum": 0, "maximum": 6},
                    "default_template": {"type": "string", "format": "uuid"},
                    "scheduling_rules": {"type": "object"}
                }
            }
        },
        "required": ["holiday_dates", "term_breaks", "config"]
    }

Fields:
- academic_year: CharField
    max_length=9
    unique=True
    db_index=True
    validators=[YearFormatValidator]
    help_text="Academic year in YYYY-YYYY format"

- start_date: DateField
    db_index=True
    help_text="First day of academic year"
    validators=[DateRangeValidator]

- end_date: DateField
    db_index=True
    help_text="Last day of academic year"
    validators=[DateRangeValidator]

- term_structure: CharField
    max_length=10
    choices=TERM_CHOICES
    db_index=True
    help_text="Academic term organization"

Inherits from MetadataModel:
- id (UUID)
- is_active (soft delete)
- created_at/modified_at
- created_by/modified_by
- metadata (with schema)
- history tracking
```

### Custom Managers
```python
class SchoolYearManager(models.Manager):
    """Primary manager for SchoolYear."""
    
    def get_current(self, date=None):
        """Returns active year containing date."""
        cache_key = f'current_year:{date or "today"}'
        # Implementation details...

class ActiveYearManager(models.Manager):
    """Filters for active school years only."""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
```

### Required Methods
```python
class SchoolYear(MetadataModel):
    # Continue class from above...

    def clean(self):
        """
        Validates:
        1. Year format and sequence
        2. Date range validity
        3. Metadata schema
        4. Term break logic
        """

    def generate_terms(self):
        """
        Creates terms based on structure.
        Called via post_save signal if no terms exist.
        
        Behaviors:
        - Semester: 2 terms, 4 quarters
        - Trimester: 3 terms
        - Respects term breaks from metadata
        - Sets correct sequence numbers
        - Maintains referential integrity
        """

    def get_current_term(self, date=None):
        """
        Returns active term for date.
        Uses caching with date-based key.
        """

    def get_week_number(self, date):
        """
        Calculates week number for date.
        Considers term breaks and holidays.
        """

    def is_school_day(self, date):
        """
        Checks if date is a valid school day.
        Excludes holidays and breaks.
        """

    class Meta:
        verbose_name = _("School Year")
        verbose_name_plural = _("School Years")
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['academic_year']),
            models.Index(fields=['start_date', 'end_date'])
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gt=F('start_date')),
                name='valid_year_dates'
            )
        ]
```

### Signals
```python
@receiver(post_save, sender=SchoolYear)
def ensure_terms_exist(sender, instance, created, **kwargs):
    """Creates terms if needed after save."""
    if created or not instance.terms.exists():
        transaction.on_commit(
            lambda: instance.generate_terms()
        )

@receiver(pre_save, sender=SchoolYear)
def validate_metadata(sender, instance, **kwargs):
    """Additional metadata validation."""
    # Implementation details...
```

### Caching
```python
CACHE_KEYS = {
    'current_year': 'school_year:current:{date}',
    'year_terms': 'school_year:{id}:terms',
    'year_term_dates': 'school_year:{id}:term_dates'
}

Cache Invalidation Points:
- save() method
- metadata updates
- term changes
- date transitions
```

### Required Tests
```python
class SchoolYearTests(TestCase):
    """
    Test suite must cover:
    1. Validation:
       - Year format
       - Date ranges
       - Metadata schema
       - Term break logic
    
    2. Term Generation:
       - Semester pattern
       - Trimester pattern
       - Quarter creation
       - Break handling
    
    3. Date Processing:
       - Week numbering
       - School day validation
       - Term date boundaries
    
    4. Caching:
       - Cache hits/misses
       - Invalidation
       - Race conditions
    
    5. History:
       - Change tracking
       - User attribution
       - Reversion
    """

class SchoolYearFactoryTests(TestCase):
    """
    Factory test coverage for:
    - Basic creation
    - With terms
    - With metadata
    - Date variations
    """
```

### Factories
```python
class SchoolYearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'calendar.SchoolYear'
    
    # Factory implementation...

class SchoolYearWithTermsFactory(SchoolYearFactory):
    """Includes generated terms."""
    
    @factory.post_generation
    def with_terms(obj, create, extracted, **kwargs):
        """Ensures terms exist."""
```

Want me to continue with the Term model specification next?