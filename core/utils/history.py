"""History tracking helper utilities."""
from typing import Any, Dict, Optional, Type
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

class SafeDeleteHistoricalModel(models.Model):
    """Base model for historical records with safe delete support."""
    
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

def get_history_model_name(model_name: str) -> str:
    """Generate historical model name."""
    return f'Historical{model_name}'

def get_history_table_name(model_name: str) -> str:
    """Generate historical table name."""
    return f'core_historical_{model_name.lower()}'

class ExtendedHistoricalRecords(HistoricalRecords):
    """Extended historical records with additional functionality."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('inherit', True)
        kwargs.setdefault('cascade_delete_history', True)
        super().__init__(*args, **kwargs)

    def post_save(self, instance: models.Model, created: bool, **kwargs: Any) -> None:
        """Custom post save to include additional metadata."""
        history_instance = self.create_historical_record(instance, created and '+' or '~')
        if history_instance is not None:
            history_instance.change_reason = getattr(instance, '_change_reason', None)
            history_instance.save()

def diff_historical_records(old: models.Model, new: models.Model) -> Dict[str, Dict[str, Any]]:
    """Compare two historical records and return differences."""
    changes = {}
    fields = new._meta.fields

    for field in fields:
        field_name = field.name
        if field_name not in ['history_id', 'history_date', 'history_change_reason']:
            old_value = getattr(old, field_name)
            new_value = getattr(new, field_name)
            if old_value != new_value:
                changes[field_name] = {
                    'old': old_value,
                    'new': new_value
                }

    return changes

def get_version_at(model: models.Model, timestamp: timezone.datetime) -> Optional[models.Model]:
    """Get model version at specific timestamp."""
    return (
        model.history.filter(history_date__lte=timestamp)
        .order_by('-history_date')
        .first()
    )
