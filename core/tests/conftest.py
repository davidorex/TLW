"""Pytest configuration and shared fixtures."""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def test_user():
    """Create and return a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_superuser():
    """Create and return a test superuser."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )

@pytest.fixture
def test_metadata_schema():
    """Return a test metadata schema."""
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "active": {"type": "boolean"}
        },
        "required": ["name"]
    }

@pytest.fixture
def test_metadata():
    """Return valid test metadata."""
    return {
        "name": "Test User",
        "age": 25,
        "active": True
    }

@pytest.fixture
def invalid_metadata():
    """Return invalid test metadata."""
    return {
        "name": 123,  # Should be string
        "age": "25",  # Should be integer
        "active": "true"  # Should be boolean
    }
