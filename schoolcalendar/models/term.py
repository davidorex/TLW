from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.db.models import Q, F
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.utils import timezone

from core.models.abstracts import MetadataModel
from .school_year import SchoolYear

# Cache key constants
CACHE_KEYS = {
    'term_weeks': 'term:{id}:weeks',
    'term_for_date': 'term:date:{date}',
    'current_term': 'term:current'
}

class TermManager(models.Manager):
    """Primary manager for Term with caching support"""
    
    def get_for_date(self, date):
        """
        Returns active term containing date with caching.
        Caches result for 24 hours.
        """
        cache_key = CACHE_KEYS['term_for_date'].format(date=date)
        
        # Try to get from cache first
        cached_term_id = cache.get(cache_key)
        if cached_term_id:
            try:
                return self.get(pk=cached_term_id)
            except self.model.DoesNotExist:
                cache.delete(cache_key)
        
        # If not in cache, query and cache
        term = self.filter(start_date__lte=date, end_date__gte=date).first()
        
        if term:
            cache.set(cache_key, term.id, timeout=86400)  # 24 hours
        
        return term

    def get_current(self):
        """
        Returns currently active term with caching.
        Caches result for 1 hour.
        """
        cache_key = CACHE_KEYS['current_term']
        
        # Try to get from cache first
        cached_term_id = cache.get(cache_key)
        if cached_term_id:
            try:
                return self.get(pk=cached_term_id)
            except self.model.DoesNotExist:
                cache.delete(cache_key)
        
        # If not in cache, query and cache
        today = timezone.now().date()
        current_term = self.get_for_date(today)
        
        if current_term:
            cache.set(cache_key, current_term.id, timeout=3600)  # 1 hour
        
        return current_term

class Term(MetadataModel):
    """
    Represents major academic periods (semester/trimester).
    Auto-generated by SchoolYear.
    Controls quarter generation for semesters.
    """

    TERM_TYPES = [
        ('SEM1', _('First Semester')),
        ('SEM2', _('Second Semester')),
        ('TRI1', _('First Trimester')),
        ('TRI2', _('Second Trimester')),
        ('TRI3', _('Third Trimester'))
    ]

    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "academic_weeks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "week_number": {"type": "integer"},
                        "start_date": {"type": "string", "format": "date"},
                        "end_date": {"type": "string", "format": "date"}
                    }
                }
            },
            "special_dates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "format": "date"},
                        "description": {"type": "string"}
                    }
                }
            }
        }
    }

    objects = TermManager()

    year = models.ForeignKey(
        SchoolYear, 
        on_delete=models.PROTECT, 
        related_name='terms',
        help_text="Associated academic year"
    )

    term_type = models.CharField(
        max_length=4, 
        choices=TERM_TYPES, 
        db_index=True,
        help_text="Type and sequence of term"
    )

    sequence = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Order within year (1-based)"
    )

    start_date = models.DateField(
        db_index=True,
        help_text="First day of term"
    )

    end_date = models.DateField(
        db_index=True,
        help_text="Last day of term"
    )

    def clean(self):
        """
        Validates:
        1. Date range within year
        2. Non-overlapping with other terms
        3. Correct sequence for type
        4. Metadata schema
        """
        # TODO: Implement comprehensive validation
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError(_("Start date must be before end date"))

    def get_weeks(self):
        """
        Returns list of week date ranges.
        Used for calendar display.
        Cached at term level.
        """
        cache_key = CACHE_KEYS['term_weeks'].format(id=self.id)
        
        # Try to get from cache first
        cached_weeks = cache.get(cache_key)
        if cached_weeks:
            return cached_weeks
        
        # Calculate weeks if not in cache
        from datetime import timedelta
        weeks = []
        current_date = self.start_date
        week_number = 1
        
        while current_date <= self.end_date:
            week_end = min(current_date + timedelta(days=6), self.end_date)
            weeks.append({
                'week_number': week_number,
                'start_date': current_date,
                'end_date': week_end
            })
            current_date += timedelta(days=7)
            week_number += 1
        
        # Cache the result
        cache.set(cache_key, weeks, timeout=86400)  # 24 hours
        
        return weeks

    def get_week_number(self, date):
        """
        Returns 1-based week number within term.
        Uses cached week boundaries.
        """
        weeks = self.get_weeks()
        for week in weeks:
            if week['start_date'] <= date <= week['end_date']:
                return week['week_number']
        return None

    # Rest of the model remains the same as in previous implementation
    # ... (previous __str__, Meta, properties remain unchanged)

# Cache invalidation signals
@receiver([post_save, post_delete], sender=Term)
def invalidate_term_caches(sender, instance, **kwargs):
    """
    Invalidates caches related to the term when saved or deleted.
    """
    # Invalidate date-based cache
    cache.delete_many([
        CACHE_KEYS['term_for_date'].format(date=instance.start_date),
        CACHE_KEYS['term_for_date'].format(date=instance.end_date),
        CACHE_KEYS['current_term'],
        CACHE_KEYS['term_weeks'].format(id=instance.id)
    ])

# Existing signals and methods remain the same