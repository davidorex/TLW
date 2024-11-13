from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.cache import cache
from django.utils import timezone

from core.models.abstracts import MetadataModel
from .term import Term

# Cache key constants
CACHE_KEYS = {
    'quarter_for_date': 'quarter:date:{date}',
    'term_quarters': 'term:{term_id}:quarters'
}

def validate_semester_term(term):
    """
    Validates that the term is a semester term.
    Raises ValidationError if not a semester term.
    """
    if not term.term_type.startswith('SEM'):
        raise ValidationError(_("Quarter can only be created for semester terms"))

class QuarterManager(models.Manager):
    """
    Custom manager for Quarter with caching support
    """
    def get_for_date(self, date, term=None):
        """
        Returns quarter containing the given date.
        Optionally filter by specific term.
        """
        cache_key = CACHE_KEYS['quarter_for_date'].format(date=date)
        
        # Try cache first
        cached_quarter_id = cache.get(cache_key)
        if cached_quarter_id:
            try:
                return self.get(pk=cached_quarter_id)
            except self.model.DoesNotExist:
                cache.delete(cache_key)
        
        # Query quarters
        query = self.filter(start_date__lte=date, end_date__gte=date)
        if term:
            query = query.filter(term=term)
        
        quarter = query.first()
        
        if quarter:
            cache.set(cache_key, quarter.id, timeout=86400)  # 24 hours
        
        return quarter

class Quarter(MetadataModel):
    """
    Represents academic quarters within a semester term.
    """

    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "reporting_dates": {
                "type": "object",
                "properties": {
                    "grades_due": {"type": "string", "format": "date"},
                    "reports_published": {"type": "string", "format": "date"},
                    "parent_meetings": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string", "format": "date"},
                            "end": {"type": "string", "format": "date"}
                        },
                        "required": ["start", "end"]
                    }
                },
                "required": ["grades_due", "reports_published", "parent_meetings"]
            },
            "assessment_weeks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "week_number": {"type": "integer", "minimum": 1},
                        "type": {"type": "string", "enum": ["formative", "summative"]}
                    },
                    "required": ["week_number", "type"]
                }
            }
        },
        "required": ["reporting_dates", "assessment_weeks"]
    }

    QUARTER_TYPES = [
        ('Q1', _('Quarter 1')),
        ('Q2', _('Quarter 2')),
        ('Q3', _('Quarter 3')),
        ('Q4', _('Quarter 4'))
    ]

    objects = QuarterManager()

    term = models.ForeignKey(
        Term, 
        on_delete=models.CASCADE, 
        related_name='quarters',
        validators=[validate_semester_term],
        help_text="Parent semester term"
    )

    quarter_type = models.CharField(
        max_length=2, 
        choices=QUARTER_TYPES,
        db_index=True,
        default='Q1'  # Added default value
    )

    sequence = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(2)
        ],
        db_index=True,
        default=1  # Added default value
    )

    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)

    def clean(self):
        """
        Comprehensive validation for Quarter
        """
        # Validate semester term
        validate_semester_term(self.term)
        
        # Validate dates
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_("Start date must be before end date"))
        
        # Validate dates within term boundaries
        if (self.start_date < self.term.start_date or 
            self.end_date > self.term.end_date):
            raise ValidationError(_("Quarter dates must be within term boundaries"))
        
        # Validate sequence
        if self.sequence not in [1, 2]:
            raise ValidationError(_("Sequence must be 1 or 2"))

    def get_week_number(self, date):
        """
        Returns the week number for a given date within the quarter.
        """
        from datetime import timedelta
        
        if not (self.start_date <= date <= self.end_date):
            return None
        
        weeks = []
        current_date = self.start_date
        week_number = 1
        
        while current_date <= self.end_date:
            week_end = min(current_date + timedelta(days=6), self.end_date)
            weeks.append({
                'start_date': current_date,
                'end_date': week_end
            })
            
            if current_date <= date <= week_end:
                return week_number
            
            current_date += timedelta(days=7)
            week_number += 1
        
        return None

    def get_reporting_dates(self):
        """
        Returns key reporting dates for the quarter.
        """
        # Placeholder implementation
        return {
            'grades_due': self.end_date,
            'reports_published': self.end_date + timezone.timedelta(days=7),
            'parent_meetings': {
                'start': self.end_date + timezone.timedelta(days=10),
                'end': self.end_date + timezone.timedelta(days=14)
            }
        }

    def __str__(self):
        return f"{self.term} - {self.get_quarter_type_display()}"

    class Meta:
        ordering = ['term', 'sequence']
        unique_together = [
            ['term', 'sequence'],
            ['term', 'quarter_type']
        ]
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['term', 'sequence'])
        ]

@receiver(pre_save, sender=Quarter)
def validate_quarter_pre_save(sender, instance, **kwargs):
    """
    Pre-save validation for Quarter
    """
    instance.clean()

@receiver(models.signals.post_save, sender=Quarter)
def invalidate_quarter_caches(sender, instance, **kwargs):
    """
    Invalidate caches related to the quarter
    """
    cache.delete_many([
        CACHE_KEYS['quarter_for_date'].format(date=instance.start_date),
        CACHE_KEYS['quarter_for_date'].format(date=instance.end_date),
        CACHE_KEYS['term_quarters'].format(term_id=instance.term_id)
    ])
