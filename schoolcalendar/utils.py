from schoolcalendar.models import PeriodTemplate

def get_default_template():
    try:
        default_template = PeriodTemplate.objects.get(is_default=True)
        return default_template.pk
    except PeriodTemplate.DoesNotExist:
        return None
