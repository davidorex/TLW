# PeriodContent Model Specification

### Base Configuration
```python
from core.models.abstracts import MetadataModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from calendar.models import PeriodTemplate
from django.utils.translation import gettext_lazy as _

Location: calendar/models/period_content.py
```

### Model Definition
```python
class PeriodContent(MetadataModel):
    """
    Stores content/events for specific periods.
    Acts as container for any schedulable content.
    Supports role-based filtering and content overrides.
    """

    CONTENT_TYPES = [
        ('CLASS', _('Class Session')),
        ('MEETING', _('Meeting')),
        ('EVENT', _('School Event')),
        ('STUDY', _('Study Period')),
        ('EXAM', _('Examination')),
        ('DUTY', _('Staff Duty')),
        ('OTHER', _('Other Activity'))
    ]

    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "visibility": {
                "type": "object",
                "properties": {
                    "roles": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "year_groups": {
                        "type": "array",
                        "items": {"type": "integer"}
                    },
                    "homerooms": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            },
            "details": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "notes": {"type": "string"},
                    "resources": {"type": "array"},
                    "requirements": {"type": "object"}
                }
            }
        }
    }

Fields:
- date: DateField
    db_index=True
    help_text="Date of period content"

- period_number: PositiveSmallIntegerField
    help_text="Period number in day schedule"
    validators=[MinValueValidator(1)]

- template: ForeignKey
    to=PeriodTemplate
    on_delete=PROTECT
    help_text="Associated period template"

- content_type: CharField
    max_length=10
    choices=CONTENT_TYPES
    help_text="Type of period content"

- priority: PositiveSmallIntegerField
    default=1
    help_text="Display/override priority"
    db_index=True

# Generic Foreign Key for content
- related_content_type: ForeignKey
    to=ContentType
    null=True
    on_delete=CASCADE

- related_object_id: UUIDField
    null=True

- content_object: GenericForeignKey
    'related_content_type'
    'related_object_id'

# Group Access Controls
- year_groups: ManyToManyField
    to='YearGroup'
    blank=True
    help_text="Visible to these year groups"

- homerooms: ManyToManyField
    to='Homeroom'
    blank=True
    help_text="Visible to these homerooms"

Inherits from MetadataModel:
- Standard tracking fields
- Metadata with schema
- History tracking
```

### Custom Managers
```python
class PeriodContentManager(models.Manager):
    """Primary manager for PeriodContent"""
    
    def for_date(self, date, user=None):
        """
        Returns visible content for date.
        Filters by user role/groups.
        Orders by priority.
        """
    
    def for_period(self, date, period_number, user=None):
        """Returns content for specific period"""
    
    def visible_to(self, user):
        """Filters content by user access"""
```

### Required Methods
```python
class PeriodContent(MetadataModel):
    # Continue class from above...

    def clean(self):
        """
        Validates:
        1. Period number validity
        2. Content type rules
        3. Access controls
        4. Metadata schema
        """

    def is_visible_to(self, user):
        """
        Checks if content visible to user.
        Considers:
        - User roles
        - Year group
        - Homeroom
        - Override rules
        """

    def get_display_data(self):
        """
        Returns formatted content for display.
        Includes:
        - Title
        - Location
        - Resources
        - Notes
        """

    @property
    def period_time(self):
        """Get time slot for period"""

    @property
    def is_override(self):
        """Check if overrides default"""

    class Meta:
        verbose_name = _("Period Content")
        verbose_name_plural = _("Period Contents")
        ordering = ['date', 'period_number', '-priority']
        indexes = [
            models.Index(fields=['date', 'period_number']),
            models.Index(fields=['content_type', 'priority'])
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(period_number__gt=0),
                name='valid_period_number'
            )
        ]
```

### Signals
```python
@receiver(pre_save, sender=PeriodContent)
def validate_visibility(sender, instance, **kwargs):
    """Ensures valid visibility settings"""

@receiver(post_save, sender=PeriodContent)
def notify_affected_users(sender, instance, created, **kwargs):
    """Notify users of schedule changes"""
```

### Caching
```python
CACHE_KEYS = {
    'period_content': 'content:date:{date}:period:{period}',
    'user_schedule': 'schedule:user:{user_id}:date:{date}',
    'group_content': 'content:group:{group_id}:date:{date}'
}

Cache Invalidation:
- Content changes
- Template changes
- Group membership changes
```

### Required Tests
```python
class PeriodContentTests(TestCase):
    """
    Test suite must cover:
    1. Content Creation:
       - Basic content
       - With generic relations
       - Different content types
       - Access controls
    
    2. Visibility Rules:
       - Role-based access
       - Group filtering
       - Override handling
    
    3. Content Resolution:
       - Priority handling
       - Multiple contents
       - Default content
    
    4. Integration:
       - Template alignment
       - User scheduling
       - Group scheduling
    
    5. Performance:
       - Efficient queries
       - Proper caching
       - Bulk operations
    """
```

### Factories
```python
class PeriodContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'calendar.PeriodContent'
    
    date = factory.LazyFunction(lambda: timezone.now().date())
    period_number = factory.Iterator(range(1, 9))
    template = factory.SubFactory(PeriodTemplateFactory)
    content_type = 'CLASS'
    priority = 1
    
    @factory.post_generation
    def year_groups(self, create, extracted, **kwargs):
        """Add year groups if specified"""
        if not create:
            return
        if extracted:
            for year_group in extracted:
                self.year_groups.add(year_group)

class OverrideContentFactory(PeriodContentFactory):
    """Creates override content"""
    content_type = 'EVENT'
    priority = 10
    metadata = factory.Dict({
        'visibility': {
            'roles': ['student', 'teacher'],
            'year_groups': [9, 10]
        },
        'details': {
            'location': 'Main Hall',
            'notes': 'School Assembly'
        }
    })
```

This provides a flexible container for any schedulable content while supporting role-based visibility and overrides. Want me to continue with any additional related models or elaborate on any part?