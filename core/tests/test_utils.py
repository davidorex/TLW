"""Test cases for core utility modules."""
from datetime import datetime, timezone
import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from ..utils.context import get_current_user, set_current_user, UserContextManager, with_user
from ..utils.metadata import MetadataValidator, validate_metadata_schema
from ..utils.history import (
    SafeDeleteHistoricalModel,
    get_history_model_name,
    get_history_table_name,
    diff_historical_records,
    get_version_at
)

User = get_user_model()

class ContextUtilsTests(TestCase):
    """Test cases for context management utilities."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_get_set_current_user(self):
        """Test getting and setting current user."""
        self.assertIsNone(get_current_user())
        set_current_user(self.user)
        self.assertEqual(get_current_user(), self.user)

    def test_user_context_manager(self):
        """Test UserContextManager functionality."""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )

        set_current_user(self.user)
        self.assertEqual(get_current_user(), self.user)

        with UserContextManager(other_user):
            self.assertEqual(get_current_user(), other_user)

        self.assertEqual(get_current_user(), self.user)

    def test_with_user_decorator(self):
        """Test with_user decorator."""
        @with_user(self.user)
        def test_func():
            return get_current_user()

        self.assertIsNone(get_current_user())
        result = test_func()
        self.assertEqual(result, self.user)
        self.assertIsNone(get_current_user())

class MetadataUtilsTests(TestCase):
    """Test cases for metadata validation utilities."""

    def setUp(self):
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "active": {"type": "boolean"}
            },
            "required": ["name"]
        }
        self.validator = MetadataValidator(self.schema)

    def test_valid_metadata(self):
        """Test validation of valid metadata."""
        data = {
            "name": "Test User",
            "age": 25,
            "active": True
        }
        validated = self.validator.validate(data)
        self.assertEqual(validated, data)

    def test_invalid_metadata_type(self):
        """Test validation with invalid data type."""
        data = {
            "name": "Test User",
            "age": "25",  # Should be integer
            "active": True
        }
        with pytest.raises(ValueError):
            self.validator.validate(data)

    def test_missing_required_field(self):
        """Test validation with missing required field."""
        data = {
            "age": 25,
            "active": True
        }
        with pytest.raises(ValueError):
            self.validator.validate(data)

    def test_validate_metadata_schema(self):
        """Test metadata schema validator."""
        with pytest.raises(ValueError):
            validate_metadata_schema("not a dict")

class HistoryUtilsTests(TestCase):
    """Test cases for history tracking utilities."""

    def test_get_history_model_name(self):
        """Test historical model name generation."""
        self.assertEqual(
            get_history_model_name("TestModel"),
            "HistoricalTestModel"
        )

    def test_get_history_table_name(self):
        """Test historical table name generation."""
        self.assertEqual(
            get_history_table_name("TestModel"),
            "core_historical_testmodel"
        )

    def test_diff_historical_records(self):
        """Test historical record comparison."""
        class MockHistoricalRecord:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        old = MockHistoricalRecord(
            name="Old Name",
            age=25,
            history_id=1,
            history_date=datetime.now(timezone.utc)
        )
        new = MockHistoricalRecord(
            name="New Name",
            age=25,
            history_id=2,
            history_date=datetime.now(timezone.utc)
        )

        diff = diff_historical_records(old, new)
        self.assertIn('name', diff)
        self.assertEqual(diff['name']['old'], "Old Name")
        self.assertEqual(diff['name']['new'], "New Name")
        self.assertNotIn('age', diff)

    def test_safe_delete_historical_model(self):
        """Test SafeDeleteHistoricalModel."""
        class TestHistoricalModel(SafeDeleteHistoricalModel):
            pass

        model = TestHistoricalModel()
        self.assertTrue(model.is_active)
        self.assertTrue(hasattr(model, 'is_active'))
