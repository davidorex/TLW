from django.db import models

class PeriodTemplateManager(models.Manager):
    def get_default(self):
        try:
            return self.get(is_default=True)
        except self.model.DoesNotExist:
            return None

class PeriodTemplate(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    objects = PeriodTemplateManager()

    def __str__(self):
        return self.name
