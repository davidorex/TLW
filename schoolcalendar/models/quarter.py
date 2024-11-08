from django.db import models
from .term import Term

class Quarter(models.Model):
    # Placeholder for Quarter model
    name = models.CharField(max_length=100)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='quarters')
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.name} - {self.term}"
