# Period Template Implementation Status
Date: 2024-02-16

## Current Implementation Details

### 1. Core Model Structure (PeriodTemplate)
```python
class PeriodTemplate(MetadataModel):
    METADATA_SCHEMA = {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "notes": {"type": "string"},
            "tags": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
```

### 2. Time Block Configuration
- Morning periods: 0-6 periods (default: 5)
- Afternoon periods: 0-6 periods (default: 4)
- Evening periods: 0-4 periods (default: 2)
- Period length: 30-120 minutes (default: 40)
- Passing time: 0-30 minutes (default: 10)
- First period start: Default 07:40

### 3. Schedule Types
- STD: Standard Day
- EXT: Extended Day
- RED: Reduced Day
- MOD: Modified Day

### 4. Data Integration Features
- JSON metadata field with schema validation
- Version control with unique_together on (name, version)
- Caching system for active templates
- Historical record tracking

### 5. Current API Endpoints
```python
urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

router.register(r'terms', TermViewSet)
router.register(r'school-years', SchoolYearViewSet)
router.register(r'period-templates', PeriodTemplateViewSet)
```

### 6. Template Manager UI
```html
<div class="period-template-manager" hx-get="{% url 'periodtemplate-list' %}" hx-trigger="load" hx-target="#templateList">
    <h2>Period Templates</h2>
    <div id="templateList">
        <!-- Dynamic content via HTMX -->
    </div>
</div>
```

### 7. Period Generation Implementation
```python
def generate_periods(self):
    """Generate periods based on template configuration."""
    periods = []
    current_time = datetime.datetime.combine(datetime.date.today(), self.first_period)
    period_number = 1

    # Generates sequential periods with:
    # - Period number
    # - Start/end times
    # - Period type (morning/afternoon/evening)
    # Returns list of period dictionaries
```

### 8. Active Template Resolution
```python
def get_active_template(self, date):
    """Get active template for given date with caching."""
    cache_key = f'template:date:{date}'
    cached_id = cache.get(cache_key)
    
    # Returns most recent template effective before given date
    # Caches result for 1 hour
```

### 9. Current Validation Rules
- Total periods must be greater than zero
- Version must be greater than existing versions
- Only one default template allowed
- Period length between 30-120 minutes
- Passing time between 0-30 minutes

### 10. Current Frontend State
- Base template with responsive navigation
- Dashboard with period template manager component
- Calendar view with placeholder content
- HTMX integration for template loading

### 11. Integration Points for Other Apps

Based on the current implementation, other apps can integrate with period containers through:

#### A. Metadata Extension
```python
# Current metadata schema allows for:
- description: string
- notes: string
- tags: array of strings

# Apps can extend this by:
1. Inheriting from MetadataModel
2. Defining their own METADATA_SCHEMA
3. Using validate_metadata_schema for validation
```

#### B. Period Access Methods
```python
# Available methods for accessing period data:
1. generate_periods() -> list of period dictionaries
2. get_period_times(number) -> dict with start/end times
3. get_active_template(date) -> template instance with caching
```

#### C. Historical Tracking
```python
# Inherited from HistoricalModel:
1. Version tracking
2. Change history
3. Revert capabilities
4. Diff comparisons
```

#### D. Core Model Features
```python
# Inherited from BaseModel:
1. UUID primary keys
2. Soft deletion
3. Timestamps
4. Active/inactive status
```

#### E. Audit Features
```python
# Inherited from AuditableModel:
1. Created by tracking
2. Modified by tracking
3. User action history
```

### 12. Example Content Integration (Quarter Model)

The Quarter model demonstrates content integration through:

```python
# Metadata Schema for Content
METADATA_SCHEMA = {
    "type": "object",
    "properties": {
        "reporting_dates": {
            "type": "object",
            "properties": {
                "grades_due": {"type": "string", "format": "date"},
                "reports_published": {"type": "string", "format": "date"}
            }
        },
        "assessment_weeks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "week_number": {"type": "integer", "minimum": 1},
                    "type": {"type": "string", "enum": ["formative", "summative"]}
                }
            }
        }
    }
}

# Time-Based Content Access
def get_for_date(self, date, term=None):
    """Returns quarter containing date with caching"""
    cache_key = f'quarter:date:{date}'
    return self.get_cached_quarter(cache_key, date, term)

def get_week_number(self, date):
    """Returns week number for content scheduling"""
    if not (self.start_date <= date <= self.end_date):
        return None
    return self.calculate_week_number(date)
