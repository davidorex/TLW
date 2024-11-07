# SchoolYear Model Specification

### Purpose
Primary container defining academic year structure. Controls term generation and schedule boundaries. Provides base calendar validation.

### Inheritance
```python
- CalendarBaseModel:
    - id: UUID (pk)
    - is_active: bool      # Soft deletion
    - created_at          # Auto timestamp
    - modified_at         # Auto timestamp
    - metadata: JSON      # Config store
    - created_by: FK      # User audit
    - modified_by: FK     # User audit
    - history            # SimpleHistoricalRecords
```

### Model Fields
```python
- academic_year: str       # "2024-2025"
                          # unique with is_active
                          # required
                          # validate YYYY-YYYY format

- start_date: date        # Year start boundary
                          # required
                          # db_index
                          
- end_date: date          # Year end boundary
                          # required
                          # db_index
                          # validate after start_date

- term_structure: str     # Choices:
                          # - SEMESTER_WITH_QUARTERS
                          # - TRIMESTER
                          # required
                          # db_index

- metadata: JSON          # Inherits from base
                          # Stores:
                          # - holiday_dates: [dates]
                          # - term_breaks: [{start,end}]
                          # - config: {settings}
```

### Meta Configuration
```python
- db_table: 'calendar_school_year'
- ordering: ['-start_date']
- unique_together: [academic_year, is_active]
- indexes: 
    - academic_year
    - (start_date, end_date)
- permissions:
    - view_calendar
    - change_calendar
    - manage_calendar_structure
```

### Required Methods
```python
# Term Management
- generate_terms()        # Creates appropriate terms on save
                         # Based on term_structure
                         # Maintains integrity with breaks

- get_current_term()     # Returns active term for given date
                         # Caches result
                         # Updates on date change

- get_term_dates()       # Returns all term boundary dates
                         # Used for term generation
                         # Considers breaks

# Validation
- clean()               # Validates:
                         # - Date ranges
                         # - Year format
                         # - Term structure
                         # - Metadata schema

- is_valid_date()       # Checks if date within bounds
                         # Considers holidays/breaks
```

### Managers
```python
- objects               # Default manager
- active               # Filters is_active=True
- current              # Returns current year by date
```

### Caching Strategy
```python
- Cache current_term
- Cache term_boundaries
- Invalidate on:
    - save()
    - metadata changes
    - date transitions
```

### Test Requirements

#### Factories
```python
BasicSchoolYearFactory:
    - Minimal valid year
    - No terms/metadata

FullSchoolYearFactory:
    - Complete year
    - With terms
    - Sample metadata

DateRangeFactory:
    - past_year
    - current_year
    - future_year
```

#### Test Cases
```python
1. Creation & Validation:
   - Valid year creation
   - Invalid date ranges
   - Format validation
   - Metadata validation

2. Term Generation:
   - Semester pattern
   - Trimester pattern
   - Break handling

3. Date Handling:
   - Current term lookup
   - Valid date checks
   - Week calculations

4. History & Audit:
   - Change tracking
   - User attribution
   - Soft deletion

5. Access Control:
   - Permission checks
   - Manager filters

6. Integration:
   - Term relationships
   - Schedule impact
   - Cache behavior
```

### Implementation Notes
1. Use Django validators for format checks
2. Implement clean caching strategy
3. Ensure proper history tracking
4. Add comprehensive docstrings
5. Include verbose_name and help_text
6. Follow i18n best practices

Want the Term model specification next?
