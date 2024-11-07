from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Core'

    def ready(self):
        import core.signals  # Register signals
        self.register_app_settings()

    def register_app_settings(self):
        """Register any app-specific settings"""
        pass  # Will be implemented as needed
