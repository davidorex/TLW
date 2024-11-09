from django.core.management.base import BaseCommand
from schoolcalendar.models import PeriodTemplate

class Command(BaseCommand):
    help = 'Ensure a default PeriodTemplate exists in the database.'

    def handle(self, *args, **options):
        try:
            default_template = PeriodTemplate.objects.get_default()
            if not default_template:
                self.stdout.write(self.style.WARNING('No default PeriodTemplate found. Creating one...'))
                # Create a default PeriodTemplate with predefined attributes
                PeriodTemplate.objects.create(name='Default Template', is_default=True)
                self.stdout.write(self.style.SUCCESS('Default PeriodTemplate created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS('Default PeriodTemplate already exists.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error ensuring default PeriodTemplate: {e}'))
