from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models.abstracts import MetadataModel
import datetime

class PeriodTemplateManager(models.Manager):
    def get_default(self):
        try:
            return self.get(is_default=True)
        except self.model.DoesNotExist:
            return None

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

    name = models.CharField(max_length=100, unique=True)
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
        return self.name

    def clean(self):
        # Validate period counts, timing, and version
        pass

    def generate_periods(self):
        # Logic to generate periods based on the template
        return []

    def create_new_version(self):
        # Logic to create a new version of the template
        return self

    def get_period_times(self, number):
        # Logic to calculate start and end times for a given number of periods
        return {}

    class Meta:
        ordering = ['-effective_from', 'name']
        indexes = [
            models.Index(fields=['effective_from', 'version']),
            models.Index(fields=['name', 'version']),
        ]
