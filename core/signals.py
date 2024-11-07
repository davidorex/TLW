from django.db.models.signals import post_save
from django.dispatch import receiver
from .registry import ContentRegistry

@receiver(post_save)
def handle_content_changes(sender, instance, **kwargs):
    """
    Generic signal handler for content changes.
    Updates period content when source changes.
    """
    if sender in ContentRegistry.get_content_types():
        # Update related period content
        # Placeholder for future implementation
        pass
