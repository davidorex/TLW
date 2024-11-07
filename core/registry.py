class ContentRegistry:
    """
    Registers content types that can be scheduled in periods.
    Provides interface for content injection.
    """
    _registry = {}

    @classmethod
    def register(cls, model_class, **options):
        """Register a model for period scheduling"""
        cls._registry[model_class] = options
        return model_class  # Allow use as a decorator

    @classmethod
    def get_content_types(cls):
        """Return all registered content types"""
        return list(cls._registry.keys())

    @classmethod
    def get_registered_models(cls):
        """Return dictionary of registered models and their options"""
        return cls._registry.copy()
