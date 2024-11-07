# PeriodTemplate Model Specification

### Base Configuration
```python
from core.models.abstracts import MetadataModel
from django.utils.translation import gettext_lazy as _

Location: calendar/models/period.py
```

### Model Definition
```python
class PeriodTemplate(MetadataModel):
    """
    Defines the daily period structure.
    Base template for school day organization.
    Supports versioning and schedule variations.
    """

    SCHEDULE_TYPES = [
        ('STD', _('Standard Day')),
        ('EXT', _('Extended Day')),  # More periods
        ('RED', _('Reduced Day')),   # Fewer periods
        ('MOD', _('Modified Day'))   # Custom structure
    ]

    PERIOD_BLOCKS = [
        ('MOR', _('Morning')),
        ('AFT', _('Afternoon')),
        ('EVE', _('Evening'))
    ]

    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "passing_time": {
                "type": "integer",  # Minutes
                "minimum": 0
            },
            "block_breaks": {
                "type": "object",
                "properties": {
                    "morning_break": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string", "format": "time"},
                            "duration": {"type": "integer"}
                        }
                    },
                    "lunch": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string", "format": "time"},
                            "duration": {"type": "integer"}
                        }
                    }
                }
            },
            "exceptions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "period_number": {"type": "integer"},
                        "custom_length": {"type": "integer"},
                        "reason": {"type": "string"}
                    }
                }
            }
        },
        "required": ["passing_time", "block_breaks"]
    }

Fields:
- name: CharField
    max_length=100
    help_text="Template identifier"

- schedule_type: CharField
    max_length=3
    choices=SCHEDULE_TYPES
    default='STD'
    help_text="Type of day schedule"

- effective_from: DateField
    help_text="When this template becomes active"
    db_index=True

- morning_periods: PositiveSmallIntegerField
    validators=[MinValueValidator(0), MaxValueValidator(6)]
    help_text="Number of morning periods"

- afternoon_periods: PositiveSmallIntegerField
    validators=[MinValueValidator(0), MaxValueValidator(6)]
    help_text="Number of afternoon periods"

- evening_periods: PositiveSmallIntegerField
    validators=[MinValueValidator(0), MaxValueValidator(4)]
    help_text="Optional evening periods"

- period_length: PositiveIntegerField
    help_text="Standard period length in minutes"
    validators=[MinValueValidator(30), MaxValueValidator(120)]

- first_period: TimeField
    help_text="Start time of first period"

- version: PositiveIntegerField
    default=1
    help_text="Template version number"
    db_index=True

Inherits from MetadataModel:
- Standard tracking fields
- Metadata with schema
- History tracking
```

### Custom Manager
```python
class PeriodTemplateManager(models.Manager):
    """Primary manager for PeriodTemplate"""
    
    def get_for_date(self, date):
        """Returns active template for date"""
        return self.filter(
            effective_from__lte=date,
            is_active=True
        ).order_by('-effective_from').first()
    
    def versions(self):
        """Returns all versions of a template"""
```

### Required Methods
```python
class PeriodTemplate(MetadataModel):
    # Continue class from above...

    def clean(self):
        """
        Validates:
        1. Period counts and timing
        2. Break scheduling
        3. Version sequence
        4. Metadata schema
        """

    def generate_periods(self):
        """
        Creates period schedule.
        Considers:
        - Standard lengths
        - Breaks
        - Exceptions
        Returns list of period dicts with times
        """

    def create_new_version(self):
        """
        Creates new version of template.
        Increments version number.
        Copies base structure.
        """

    def get_period_time(self, period_number):
        """
        Returns start/end times for period.
        Considers exceptions.
        """

    @property
    def total_periods(self):
        """Sum of all periods"""

    @property
    def schedule_duration(self):
        """Total minutes in school day"""

    class Meta:
        verbose_name = _("Period Template")
        verbose_name_plural = _("Period Templates")
        ordering = ['-effective_from', '-version']
        indexes = [
            models.Index(fields=['effective_from', 'version']),
            models.Index(fields=['schedule_type'])
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(total_periods__gt=0),
                name='at_least_one_period'
            )
        ]
```

### Signals
```python
@receiver(pre_save, sender=PeriodTemplate)
def validate_schedule(sender, instance, **kwargs):
    """Ensures schedule timing validity"""

@receiver(post_save, sender=PeriodTemplate)
def invalidate_caches(sender, instance, **kwargs):
    """Clears cached schedules"""
```

### Caching
```python
CACHE_KEYS = {
    'active_template': 'template:date:{date}',
    'period_schedule': 'template:{id}:periods',
    'template_versions': 'template:{name}:versions'
}

Cache Invalidation:
- Template changes
- Version creation
- Metadata updates
```

### Required Tests
```python
class PeriodTemplateTests(TestCase):
    """
    Test suite must cover:
    1. Template Creation:
       - Period counts
       - Time calculations
       - Break scheduling
       - Version control
    
    2. Schedule Generation:
       - Period timing
       - Break inclusion
       - Exception handling
    
    3. Validation:
       - Time constraints
       - Period counts
       - Break timing
       - Version sequence
    
    4. Version Control:
       - Version increment
       - History tracking
       - Effective dates
    
    5. Integration:
       - Day scheduling
       - Override handling
    """
```

### Factories
```python
class PeriodTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'calendar.PeriodTemplate'
    
    name = factory.Sequence(lambda n: f"Schedule Template {n}")
    schedule_type = 'STD'
    morning_periods = 4
    afternoon_periods = 4
    evening_periods = 0
    period_length = 45
    first_period = time(8, 0)  # 8:00 AM
    
    @factory.post_generation
    def with_metadata(obj, create, extracted, **kwargs):
        """Adds standard break structure"""
        if create:
            obj.metadata = {
                "passing_time": 5,
                "block_breaks": {
                    "morning_break": {
                        "start": "10:15",
                        "duration": 15
                    },
                    "lunch": {
                        "start": "12:00",
                        "duration": 45
                    }
                },
                "exceptions": []
            }
            obj.save()

class ModifiedTemplateFactory(PeriodTemplateFactory):
    """Template with custom period structure"""
    schedule_type = 'MOD'
    # Custom period counts and exceptions
```

Want me to continue with the Day (PeriodContent) model specification next?