"""User context management utilities."""
from typing import Optional
from django.contrib.auth import get_user_model
from threading import local

User = get_user_model()
_thread_locals = local()

def get_current_user() -> Optional[User]:
    """Get the current user from thread local storage."""
    return getattr(_thread_locals, 'user', None)

def set_current_user(user: Optional[User]) -> None:
    """Set the current user in thread local storage."""
    _thread_locals.user = user

class UserContextManager:
    """Context manager for handling user context."""
    
    def __init__(self, user: Optional[User]):
        self.user = user
        self.previous_user = None

    def __enter__(self):
        self.previous_user = get_current_user()
        set_current_user(self.user)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        set_current_user(self.previous_user)

def with_user(user: Optional[User]):
    """Decorator to set user context for a function."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with UserContextManager(user):
                return func(*args, **kwargs)
        return wrapper
    return decorator
