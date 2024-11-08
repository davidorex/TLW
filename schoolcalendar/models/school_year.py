from django.db import models

class SchoolYear(models.Model):
    # Placeholder for SchoolYear model
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name
