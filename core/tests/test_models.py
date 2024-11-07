"""Test cases for core abstract models."""
from datetime import datetime, timezone
import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db import models
from ..models.abstracts import (
    BaseModel,
    AuditableModel,
    HistoricalModel,
    MetadataModel
)
from ..utils.context import UserContextManager

User = get_user_model()

class TestBaseModel(BaseModel):
    """Concrete model for testing BaseModel."""
    name = models.CharField(max_length=100)

    class Meta(BaseModel.Meta):
        abstract = False

class BaseModelTests(TestCase):
    """Test cases for BaseModel functionality."""

    def setUp(self):
        self.model = TestBaseModel.objects.create(name="Test Instance")

    def test_uuid_generation(self):
        """Test UUID field generation."""
        self.assertIsNotNone(self.model.id)
        self.assertEqual(len(str(self.model.id)), 36)  # UUID length

    def test_timestamp_fields(self):
        """Test automatic timestamp fields."""
        self.assertIsNotNone(self.model.created_at)
        self.assertIsNotNone(self.model.modified_at)

    def test_soft_delete(self):
        """Test soft deletion functionality."""
        self.assertTrue(self.model.is_active)
        self.model.soft_delete()
        self.assertFalse(self.model.is_active)
        self.assertTrue(self.model.is_deleted)

    def test_restore(self):
        """Test restoration of soft-deleted instance."""
        self.model.soft_delete()
        self.model.restore()
        self.assertTrue(self.model.is_active)
        self.assertFalse(self.model.is_deleted)

    def test_active_manager(self):
        """Test active manager filtering."""
        TestBaseModel.objects.create(name="Active Instance")
        inactive = TestBaseModel.objects.create(name="Inactive Instance")
        inactive.soft_delete()

        self.assertEqual(TestBaseModel.objects.count(), 3)
        self.assertEqual(TestBaseModel.active.count(), 2)

class TestAuditableModel(AuditableModel):
    """Concrete model for testing AuditableModel."""
    name = models.CharField(max_length=100)

    class Meta(AuditableModel.Meta):
        abstract = False

class AuditableModelTests(TestCase):
    """Test cases for AuditableModel functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )

    def test_user_tracking(self):
        """Test user tracking on creation and modification."""
        with UserContextManager(self.user):
            instance = TestAuditableModel.objects.create(name="Test Instance")
            self.assertEqual(instance.created_by, self.user)
            self.assertEqual(instance.modified_by, self.user)

            with UserContextManager(self.other_user):
                instance.name = "Updated Name"
                instance.save()
                self.assertEqual(instance.created_by, self.user)
                self.assertEqual(instance.modified_by, self.other_user)

    def test_user_name_methods(self):
        """Test user name representation methods."""
        with UserContextManager(self.user):
            instance = TestAuditableModel.objects.create(name="Test Instance")
            self.assertEqual(instance.get_creator_name(), str(self.user))
            self.assertEqual(instance.get_modifier_name(), str(self.user))

class TestHistoricalModel(HistoricalModel):
    """Concrete model for testing HistoricalModel."""
    name = models.CharField(max_length=100)

    class Meta(HistoricalModel.Meta):
        abstract = False

class HistoricalModelTests(TestCase):
    """Test cases for HistoricalModel functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        with UserContextManager(self.user):
            self.instance = TestHistoricalModel.objects.create(
                name="Original Name"
            )

    def test_history_tracking(self):
        """Test history tracking functionality."""
        self.assertEqual(self.instance.history.count(), 1)
        self.instance.name = "Updated Name"
        self.instance._change_reason = "Name updated"
        self.instance.save()
        self.assertEqual(self.instance.history.count(), 2)

    def test_revert_to(self):
        """Test reverting to previous version."""
        original_name = self.instance.name
        self.instance.name = "Updated Name"
        self.instance.save()
        
        first_version = self.instance.history.first()
        self.instance.revert_to(first_version.history_id)
        self.assertEqual(self.instance.name, original_name)

    def test_version_comparison(self):
        """Test version comparison functionality."""
        original_version = self.instance.history.latest()
        self.instance.name = "Updated Name"
        self.instance.save()

        diff = self.instance.diff_with(original_version)
        self.assertIn('name', diff)
        self.assertEqual(diff['name']['old'], "Original Name")
        self.assertEqual(diff['name']['new'], "Updated Name")

class TestMetadataModel(MetadataModel):
    """Concrete model for testing MetadataModel."""
    name = models.CharField(max_length=100)

    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "key": {"type": "string"},
            "value": {"type": "integer"}
        }
    }

    class Meta(MetadataModel.Meta):
        abstract = False

class MetadataModelTests(TestCase):
    """Test cases for MetadataModel functionality."""

    def setUp(self):
        self.instance = TestMetadataModel.objects.create(
            name="Test Instance",
            metadata={"key": "test", "value": 123}
        )

    def test_metadata_validation(self):
        """Test metadata validation."""
        # Valid update
        self.instance.update_metadata({"key": "new", "value": 456})
        self.assertEqual(self.instance.get_metadata("key"), "new")
        self.assertEqual(self.instance.get_metadata("value"), 456)

        # Invalid update
        with pytest.raises(ValueError):
            self.instance.update_metadata({"key": "test", "value": "invalid"})

    def test_metadata_properties(self):
        """Test metadata properties."""
        self.assertTrue(self.instance.has_metadata)
        self.assertTrue(self.instance.valid_metadata)
        self.assertEqual(self.instance.metadata_schema, TestMetadataModel.METADATA_SCHEMA)

    def test_metadata_methods(self):
        """Test metadata access methods."""
        self.assertEqual(self.instance.get_metadata("key"), "test")
        self.assertEqual(self.instance.get_metadata("nonexistent", "default"), "default")

        self.instance.set_metadata("key", "updated")
        self.assertEqual(self.instance.get_metadata("key"), "updated")
