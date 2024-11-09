from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import logging
from .period_template import PeriodTemplate

logger = logging.getLogger(__name__)

def get_default_template():
    """
    Returns the default template's primary key if it exists, otherwise returns None.
    Uses the PeriodTemplate manager's get_default method for consistency.
    Logs a warning if no default template is found.
    """
    try:
        default_template = PeriodTemplate.objects.get_default()
        if default_template:
            return default_template.pk
        logger.warning("No default PeriodTemplate found in the database")
        return None
    except PeriodTemplate.DoesNotExist:
        logger.warning("Error retrieving default PeriodTemplate", exc_info=True)
        return None

class PeriodContent(models.Model):
    date = models.DateField(db_index=True, default=timezone.now)
    period_number = models.PositiveSmallIntegerField(db_index=True, default=1)
    template = models.ForeignKey(
        PeriodTemplate,
        on_delete=models.PROTECT,
        null=True,
        default=get_default_template
    )
    content_type = models.CharField(
        max_length=10,
        choices=[
            ("CLASS", "Class Session"),
            ("MEETING", "Meeting"),
            ("EVENT", "School Event"),
            ("STUDY", "Study Period"),
            ("EXAM", "Examination"),
            ("DUTY", "Staff Duty"),
            ("OTHER", "Other Activity")
        ],
        db_index=True,
        default="OTHER"
    )
    display_mode = models.CharField(
        max_length=10,
        choices=[
            ("SCHEDULE", "Schedule View"),
            ("STANDALONE", "Standalone View")
        ],
        default="SCHEDULE"
    )
    priority = models.PositiveSmallIntegerField(default=1, db_index=True)
    related_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    related_object_id = models.UUIDField(null=True, blank=True)
    content_object = GenericForeignKey('related_content_type', 'related_object_id')
    # year_groups = models.ManyToManyField('app_label.YearGroup', blank=True)
    # homerooms = models.ManyToManyField('app_label.Homeroom', blank=True)

    def clean(self):
        # Validate period_number, content_type, access
        pass

    def is_visible_to(self, user):
        # Logic to determine visibility to a user
        return True

    def resolve_conflicts(self):
        # Logic to resolve conflicts
        return []

    def get_display_data(self):
        # Logic to get display data
        return {}

    class Meta:
        ordering = ["date", "period_number", "-priority"]
        indexes = [
            models.Index(fields=["date", "period_number"]),
            models.Index(fields=["content_type", "priority"])
        ]

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

@receiver(pre_save, sender=PeriodContent)
def validate_scheduling(sender, instance, **kwargs):
    # Logic to validate scheduling
    pass

@receiver(post_save, sender=PeriodContent)
def notify_users(sender, instance, created, **kwargs):
    # Logic to notify users
    pass

# Caching keys
CACHE_KEYS = {
    'period_content': 'content:date:{date}:period:{period}',
    'user_schedule': 'schedule:user:{user_id}:date:{date}',
    'group_content': 'content:group:{group_id}:date:{date}'
}
