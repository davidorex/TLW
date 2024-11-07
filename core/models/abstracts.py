"""Core abstract models."""
import uuid
from typing import Any, Dict, Optional
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoLastModifiedField, AutoCreatedField
from safedelete.models import SafeDeleteModel
from safedelete.managers import SafeDeleteManager
from simple_history.models import HistoricalRecords
from ..utils.metadata import validate_metadata_schema
from ..utils.context import get_current_user
from ..utils.history import (
    SafeDeleteHistoricalModel,
    ExtendedHistoricalRecords,
    diff_historical_records,
    get_version_at
)

class BaseManager(SafeDeleteManager):
    """Base manager for all models."""
    pass

class ActiveManager(BaseManager):
    """Manager that only returns active instances."""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class BaseModel(SafeDeleteModel):
    """Base model for all system models."""
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        help_text=_("Unique identifier for this object")
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text=_("Soft deletion status")
    )

    created_at = AutoCreatedField(
        db_index=True,
        help_text=_("Timestamp when object was created")
    )

    modified_at = AutoLastModifiedField(
        help_text=_("Timestamp when object was last modified")
    )

    objects = BaseManager()
    active = ActiveManager()

    class Meta:
        abstract = True
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at', 'is_active'])
        ]

    @property
    def is_deleted(self) -> bool:
        """Check if instance is deleted."""
        return not self.is_active

    @property
    def active_status(self) -> str:
        """Get human-readable active status."""
        return "Active" if self.is_active else "Inactive"

    def soft_delete(self, using=None):
        """Soft delete the instance."""
        self.is_active = False
        self.save(using=using)

    def restore(self, using=None):
        """Restore a soft-deleted instance."""
        self.is_active = True
        self.save(using=using)

class AuditableModel(BaseModel):
    """Model with user action tracking."""

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        help_text=_("User who created this object")
    )

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_modified",
        help_text=_("User who last modified this object")
    )

    class Meta(BaseModel.Meta):
        abstract = True

    def save(self, *args, **kwargs):
        """Update user fields from context."""
        user = kwargs.pop('user', None) or get_current_user()
        
        if user:
            if not self.pk:  # New instance
                self.created_by = user
            self.modified_by = user
            
        super().save(*args, **kwargs)

    def get_creator_name(self) -> str:
        """Get string representation of creator."""
        return str(self.created_by) if self.created_by else "Unknown"

    def get_modifier_name(self) -> str:
        """Get string representation of last modifier."""
        return str(self.modified_by) if self.modified_by else "Unknown"

class HistoricalModel(AuditableModel):
    """Model with change tracking and versioning."""

    change_reason = models.CharField(
        max_length=255,
        null=True,
        help_text=_("Reason for this change")
    )

    history = ExtendedHistoricalRecords(
        inherit=True,
        cascade_delete_history=True,
        user_model=settings.AUTH_USER_MODEL,
        table_name='core_historical_%(class)s',
        custom_model_name=lambda x: f'Historical{x}',
        excluded_fields=['modified_at'],
        bases=[SafeDeleteHistoricalModel]
    )

    class Meta(AuditableModel.Meta):
        abstract = True

    def get_history_type_display(self) -> str:
        """Get human-readable history type."""
        history_types = {
            '+': 'Created',
            '~': 'Modified',
            '-': 'Deleted'
        }
        latest = self.history.latest()
        return history_types.get(latest.history_type, 'Unknown')

    def revert_to(self, history_id: int) -> None:
        """Revert to a specific historical version."""
        historical_instance = self.history.get(history_id=history_id)
        for field in self._meta.fields:
            if field.name not in ['id', 'created_at', 'modified_at']:
                setattr(self, field.name, getattr(historical_instance, field.name))
        self._change_reason = f"Reverted to version from {historical_instance.history_date}"
        self.save()

    def get_version_at(self, timestamp):
        """Get version at specific timestamp."""
        return get_version_at(self, timestamp)

    def diff_with(self, other_version) -> Dict[str, Dict[str, Any]]:
        """Compare with another version."""
        return diff_historical_records(other_version, self)

    @property
    def previous_version(self):
        """Get previous version."""
        return self.history.filter(history_date__lt=self.modified_at).first()

    @property
    def next_version(self):
        """Get next version."""
        return self.history.filter(history_date__gt=self.modified_at).last()

    @property
    def has_changes(self) -> bool:
        """Check if instance has any changes."""
        return self.history.count() > 1

class MetadataModel(HistoricalModel):
    """Model with flexible metadata storage and validation."""

    metadata = models.JSONField(
        default=dict,
        validators=[validate_metadata_schema],
        help_text=_("JSON metadata storage")
    )

    class Meta(HistoricalModel.Meta):
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'METADATA_SCHEMA'):
            raise ValueError(f"{self.__class__.__name__} must define METADATA_SCHEMA")

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value for key."""
        return self.metadata.get(key, default)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set single metadata value."""
        self.metadata[key] = value
        self.validate_metadata()
        self.save()

    def update_metadata(self, data_dict: Dict[str, Any]) -> None:
        """Bulk update metadata."""
        self.metadata.update(data_dict)
        self.validate_metadata()
        self.save()

    def validate_metadata(self) -> None:
        """Validate full metadata against schema."""
        validate_metadata_schema(self.metadata)

    @property
    def metadata_schema(self) -> Dict[str, Any]:
        """Get metadata schema."""
        return self.METADATA_SCHEMA

    @property
    def has_metadata(self) -> bool:
        """Check if instance has any metadata."""
        return bool(self.metadata)

    @property
    def valid_metadata(self) -> bool:
        """Check if metadata is valid."""
        try:
            self.validate_metadata()
            return True
        except ValueError:
            return False
