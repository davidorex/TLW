from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.models.abstracts import MetadataModel
import datetime
import copy

class PeriodTemplateManager(models.Manager):
    def get_default(self):
        try:
            return self.get(is_default=True)
        except self.model.DoesNotExist:
            return None

    def get_active_template(self, date):
        """Get active template for given date with caching."""
        cache_key = f'template:date:{date}'
        cached_id = cache.get(cache_key)
        
        if cached_id:
            try:
                return self.get(pk=cached_id)
            except self.model.DoesNotExist:
                cache.delete(cache_key)
        
        template = (
            self.filter(effective_from__lte=date)
            .order_by('-effective_from', '-version')
            .first()
        )
        
        if template:
            cache.set(cache_key, template.id, timeout=3600)  # Cache for 1 hour
        
        return template

class PeriodTemplate(MetadataModel):
    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "notes": {"type": "string"},
            "tags": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }

    SCHEDULE_TYPES = [
        ('STD', 'Standard Day'),
        ('EXT', 'Extended Day'),
        ('RED', 'Reduced Day'),
        ('MOD', 'Modified Day'),
    ]

    name = models.CharField(max_length=100)  # Removed unique=True
    schedule_type = models.CharField(max_length=3, choices=SCHEDULE_TYPES, default='STD', db_index=True)
    effective_from = models.DateField(db_index=True, default=datetime.date.today)
    morning_periods = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)], default=5)
    afternoon_periods = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)], default=4)
    evening_periods = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)], default=2)
    period_length = models.PositiveIntegerField(validators=[MinValueValidator(30), MaxValueValidator(120)], default=40)
    passing_time = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], default=10)
    first_period = models.TimeField(default=datetime.time(7, 40))
    is_default = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1, db_index=True)

    objects = PeriodTemplateManager()

    def __str__(self):
        return f"{self.name} (v{self.version})"

    def clean(self):
        """Validate period counts, timing, and version."""
        if self.morning_periods + self.afternoon_periods + self.evening_periods == 0:
            raise ValidationError("At least one period must be defined")
        
        # Check version constraint
        if self.pk is None:  # New instance
            existing = PeriodTemplate.objects.filter(name=self.name).order_by('-version').first()
            if existing and self.version <= existing.version:
                raise ValidationError("Version must be greater than existing versions")

    def generate_periods(self):
        """Generate periods based on the template configuration."""
        periods = []
        current_time = datetime.datetime.combine(datetime.date.today(), self.first_period)
        period_number = 1

        # Morning periods
        for i in range(self.morning_periods):
            start_time = current_time.time()
            end_time = (current_time + datetime.timedelta(minutes=self.period_length)).time()
            periods.append({
                'number': period_number,
                'start_time': start_time,
                'end_time': end_time,
                'type': 'morning'
            })
            period_number += 1
            current_time += datetime.timedelta(minutes=self.period_length + self.passing_time)

        # Afternoon periods
        for i in range(self.afternoon_periods):
            start_time = current_time.time()
            end_time = (current_time + datetime.timedelta(minutes=self.period_length)).time()
            periods.append({
                'number': period_number,
                'start_time': start_time,
                'end_time': end_time,
                'type': 'afternoon'
            })
            period_number += 1
            current_time += datetime.timedelta(minutes=self.period_length + self.passing_time)

        # Evening periods
        for i in range(self.evening_periods):
            start_time = current_time.time()
            end_time = (current_time + datetime.timedelta(minutes=self.period_length)).time()
            periods.append({
                'number': period_number,
                'start_time': start_time,
                'end_time': end_time,
                'type': 'evening'
            })
            period_number += 1
            current_time += datetime.timedelta(minutes=self.period_length + self.passing_time)

        return periods

    def create_new_version(self):
        """Create a new version of the template."""
        # Get the highest version number for this template name
        latest = PeriodTemplate.objects.filter(name=self.name).order_by('-version').first()
        next_version = (latest.version + 1) if latest else 1

        new_template = copy.copy(self)
        new_template.pk = None
        new_template.version = next_version
        new_template._state.adding = True
        new_template.save()
        return new_template

    def get_period_times(self, number):
        """Calculate start and end times for a given period number."""
        periods = self.generate_periods()
        for period in periods:
            if period['number'] == number:
                return {
                    'start_time': period['start_time'],
                    'end_time': period['end_time']
                }
        return {}

    class Meta:
        ordering = ['-effective_from', 'name']
        indexes = [
            models.Index(fields=['effective_from', 'version']),
            models.Index(fields=['name', 'version']),
        ]
        unique_together = [('name', 'version')]  # Added unique_together constraint

@receiver(pre_save, sender=PeriodTemplate)
def handle_default_template(sender, instance, **kwargs):
    """Ensure only one default template exists."""
    if instance.is_default:
        # Unset any existing default templates
        PeriodTemplate.objects.filter(is_default=True).exclude(pk=instance.pk).update(is_default=False)
