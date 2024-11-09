from django.db import models
from django.utils.translation import gettext_lazy as _

class SchoolYear(models.Model):
    TERM_TYPES = [
        ('SEMESTER', _('Semester')),
        ('TRIMESTER', _('Trimester'))
    ]

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    term_type = models.CharField(
        max_length=10, 
        choices=TERM_TYPES, 
        default='SEMESTER'
    )
    
    def __str__(self):
        return self.name
