from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta, datetime

from core.models.abstracts import MetadataModel

# Cache key constants
CACHE_KEYS = {
    'active_template': 'template:date:{date}',
    'period_schedule': 'template:{id}:periods',
    'template_versions': 'template:{name}:versions'
}

class PeriodTemplateManager(models.Manager):
    """
    Custom manager for PeriodTemplate with caching support
    """
    def get_active_template(self, date=None):
        """
        Returns the active template for a given date.
        If no date provided, uses current date.
        """
        if date is None:
            date = timezone.now().date()
        
        cache_key = CACHE_KEYS['active_template'].format(date=date)
        
        # Try cache first
        cached_template_id = cache.get(cache_key)
        if cached_template_id:
            try:
                return self.get(pk=cached_template_id)
            except self.model.DoesNotExist:
                cache.delete(cache_key)
        
        # Query active template
        template = self.filter(
            effective_from__lte=date
        ).order_by('-effective_from', '-version').first()
        
        if template:
            cache.set(cache_key, template.id, timeout=86400)  # 24 hours
        
        return template

class PeriodTemplate(MetadataModel):
    """
    Represents a template for daily academic periods.
    Supports different schedule types and versioning.
    """

    SCHEDULE_TYPES = [
        ('STD', _('Standard Day')),
        ('EXT', _('Extended Day')),
        ('RED', _('Reduced Day')),
        ('MOD', _('Modified Day'))
    ]

    objects = PeriodTemplateManager()

    name = models.CharField(
        max_length=100, 
        unique=True
    )

    schedule_type = models.CharField(
        max_length=3, 
        choices=SCHEDULE_TYPES,
        default='STD',
        db_index=True
    )

    effective_from = models.DateField(
        db_index=True,
        default=timezone.now  # Added default value using current date
    )

    morning_periods = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(6)
        ],
        default=3
    )

    afternoon_periods = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(6)
        ],
        default=2
    )

    evening_periods = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4)
        ],
        default=0
    )

    period_length = models.PositiveIntegerField(
        validators=[
            MinValueValidator(30),
            MaxValueValidator(120)
        ],
        default=45
    )

    passing_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(30)
        ],
        default=5
    )

    first_period = models.TimeField(
        default=timezone.now
    )

    version = models.PositiveIntegerField(
        default=1,
        db_index=True
    )

    def clean(self):
        """
        Comprehensive validation for PeriodTemplate
        """
        # Validate period counts
        total_periods = self.morning_periods + self.afternoon_periods + self.evening_periods
        if total_periods == 0:
            raise ValidationError(_("At least one period must be defined"))
        
        # Validate timing
        if self.period_length < 30 or self.period_length > 120:
            raise ValidationError(_("Period length must be between 30 and 120 minutes"))
        
        # Validate version
        existing_templates = PeriodTemplate.objects.filter(
            name=self.name
        ).exclude(pk=self.pk)
        
        max_version = existing_templates.aggregate(
            models.Max('version')
        )['version__max'] or 0
        
        if self.version <= max_version:
            raise ValidationError(_("Version must be higher than existing versions"))

    def generate_periods(self):
        """
        Generates a list of periods with their start and end times
        """
        periods = []
        current_time = datetime.combine(datetime.today(), self.first_period)
        
        # Morning periods
        for i in range(1, self.morning_periods + 1):
            period_start = current_time
            period_end = period_start + timedelta(minutes=self.period_length)
            periods.append({
                'number': i,
                'type': 'morning',
                'start_time': period_start.time(),
                'end_time': period_end.time()
            })
            current_time = period_end + timedelta(minutes=self.passing_time)
        
        # Afternoon periods
        for i in range(1, self.afternoon_periods + 1):
            period_start = current_time
            period_end = period_start + timedelta(minutes=self.period_length)
            periods.append({
                'number': self.morning_periods + i,
                'type': 'afternoon',
                'start_time': period_start.time(),
                'end_time': period_end.time()
            })
            current_time = period_end + timedelta(minutes=self.passing_time)
        
        # Evening periods
        for i in range(1, self.evening_periods + 1):
            period_start = current_time
            period_end = period_start + timedelta(minutes=self.period_length)
            periods.append({
                'number': self.morning_periods + self.afternoon_periods + i,
                'type': 'evening',
                'start_time': period_start.time(),
                'end_time': period_end.time()
            })
            current_time = period_end + timedelta(minutes=self.passing_time)
        
        return periods

    def create_new_version(self):
        """
        Creates a new version of the current template
        """
        # Get the latest version
        latest_version = PeriodTemplate.objects.filter(
            name=self.name
        ).aggregate(models.Max('version'))['version__max'] or 0
        
        # Create a new instance with incremented version
        new_template = PeriodTemplate.objects.create(
            name=self.name,
            schedule_type=self.schedule_type,
            effective_from=timezone.now().date(),
            morning_periods=self.morning_periods,
            afternoon_periods=self.afternoon_periods,
            evening_periods=self.evening_periods,
            period_length=self.period_length,
            passing_time=self.passing_time,
            first_period=self.first_period,
            version=latest_version + 1
        )
        
        return new_template

    def get_period_times(self, number):
        """
        Returns start and end times for a specific period number
        """
        periods = self.generate_periods()
        
        for period in periods:
            if period['number'] == number:
                return {
                    'start_time': period['start_time'],
                    'end_time': period['end_time']
                }
        
        raise ValueError(f"Period {number} not found in template")

    def __str__(self):
        return f"{self.name} (v{self.version})"

    class Meta:
        ordering = ['-effective_from', 'name']
        indexes = [
            models.Index(fields=['effective_from', 'version']),
            models.Index(fields=['name', 'version'])
        ]

@receiver(pre_save, sender=PeriodTemplate)
def validate_schedule(sender, instance, **kwargs):
    """
    Pre-save validation for PeriodTemplate
    """
    instance.clean()

@receiver(post_save, sender=PeriodTemplate)
def clear_caches(sender, instance, **kwargs):
    """
    Clear caches related to the period template
    """
    cache.delete_many([
        CACHE_KEYS['active_template'].format(date=timezone.now().date()),
        CACHE_KEYS['period_schedule'].format(id=instance.id),
        CACHE_KEYS['template_versions'].format(name=instance.name)
    ])
