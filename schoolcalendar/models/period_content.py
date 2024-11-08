from django.db import models
from .period_template import PeriodTemplate

class PeriodContent(models.Model):
    # Placeholder for PeriodContent model
    period_template = models.ForeignKey(PeriodTemplate, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=100)
    content_id = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.content_type} - {self.period_template}"

    class Meta:
        unique_together = ('content_type', 'content_id', 'period_template')
