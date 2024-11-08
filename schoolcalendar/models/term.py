from django.db import models
from .school_year import SchoolYear

class Term(models.Model):
    # Placeholder for Term model
    name = models.CharField(max_length=100)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, related_name='terms')
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.name} - {self.school_year}"
