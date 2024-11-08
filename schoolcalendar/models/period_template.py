from django.db import models
from .quarter import Quarter

class PeriodTemplate(models.Model):
    # Placeholder for PeriodTemplate model
    name = models.CharField(max_length=100)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, related_name='period_templates')
    duration = models.DurationField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.quarter}"
