# SchoolYear Model Changes

## Before Changes
```python
class SchoolYear(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name
```

## After Changes
```python
class SchoolYear(models.Model):
    TERM_STRUCTURES = [
        ('SEMESTER', _('Semester')),
        ('TRIMESTER', _('Trimester'))
    ]

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    term_structure = models.CharField(
        max_length=10, 
        choices=TERM_STRUCTURES, 
        default='SEMESTER'
    )
    
    def __str__(self):
        return self.name
```

## Key Changes
1. Added `TERM_STRUCTURES` class-level choices
2. Added `term_structure` field with:
   - CharField type
   - Maximum length of 10
   - Choices from `TERM_STRUCTURES`
   - Default value of 'SEMESTER'
3. Imported `gettext_lazy as _` for internationalization of choices

## Rationale
- Provides explicit definition of possible term structures
- Allows specifying term structure for each school year
- Supports both semester and trimester academic calendars
- Provides a default value to ensure data consistency
- Enables internationalization of choice labels
