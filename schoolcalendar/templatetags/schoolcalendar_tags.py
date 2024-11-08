from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_calendar_component(component_name, *args, **kwargs):
    """
    Placeholder for rendering calendar-specific components
    """
    return mark_safe(f'<!-- Rendered {component_name} component -->')

@register.filter
def format_calendar_date(value, format_string='%Y-%m-%d'):
    """
    Custom filter to format dates in calendar views
    """
    try:
        return value.strftime(format_string)
    except (AttributeError, ValueError):
        return value
