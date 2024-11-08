from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SchoolCalendarConfig(AppConfig):
    name = 'schoolcalendar'
    verbose_name = _('School Calendar')
    
    def ready(self):
        import schoolcalendar.signals
        from core.registry import ContentRegistry
        from . import models

        # Register calendar models using the existing register method
        ContentRegistry.register(models.SchoolYear)
        ContentRegistry.register(models.Term)
        ContentRegistry.register(models.Quarter)
        ContentRegistry.register(models.PeriodTemplate)
        ContentRegistry.register(models.PeriodContent)

        self.setup_cache_config()

    def setup_cache_config(self):
        from django.core.cache import cache
        cache.set_many({
            'CALENDAR_CACHE_VERSION': '2.0',
            'CALENDAR_CACHE_TIMEOUT': 3600,
        })
