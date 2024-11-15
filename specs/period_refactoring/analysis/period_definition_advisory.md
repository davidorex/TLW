# Advisory: PeriodTemplate to PeriodDefinition Transition

## Current Implementation Analysis

### Existing Limitations
1. Fixed Period Structure
```python
# Current: All periods in template must have same length
period_length = models.PositiveIntegerField(default=40)
```

2. Rigid Period Categories
```python
# Current: Fixed morning/afternoon/evening structure
morning_periods = models.PositiveSmallIntegerField(default=5)
afternoon_periods = models.PositiveSmallIntegerField(default=4)
evening_periods = models.PositiveSmallIntegerField(default=2)
```

3. Complex Period Generation
```python
# Current: Complex calculation of period times
def generate_periods(self):
    current_time = datetime.datetime.combine(datetime.date.today(), self.first_period)
    period_number = 1
    # Complex loops for morning/afternoon/evening...
```

## Proposed Solution Benefits

### 1. Improved Data Model
```python
class PeriodDefinition(models.Model):
    template = models.ForeignKey('PeriodTemplate')
    number = models.IntegerField()
    length = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(120)]
    )
    start = models.TimeField()
    type = models.CharField(max_length=10)
    passing = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(30)]
    )
    meta = models.JSONField(default=dict)
```

Benefits:
- Direct representation of period attributes
- Flexible period lengths
- Explicit start times vs calculations
- Per-period metadata
- Customizable passing times

### 2. Technical Advantages
- Eliminates period generation complexity
- Reduces race conditions
- Simpler caching (cache individual periods)
- Better query optimization potential
- More maintainable code

### 3. Feature Improvements
- Support for variable length periods
- Non-sequential period numbers possible
- Gaps between periods allowed
- Custom period types
- Per-period metadata storage

## Implementation Recommendations

### 1. Development Approach
Since this is in local development:
- Create new model in single migration
- No need for complex data migration
- Can rebuild development database
- Focus on getting design right

### 2. Key Steps
```python
# 1. Create model with proper constraints
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['template', 'number'],
            name='unique_period_per_template'
        )
    ]

# 2. Add helper methods for common operations
def get_end_time(self):
    return (datetime.datetime.combine(
        datetime.date.today(), 
        self.start
    ) + datetime.timedelta(
        minutes=self.length
    )).time()

# 3. Add validation
def clean(self):
    if self.start and self.length:
        end_time = self.get_end_time()
        # Add validation logic...
```

### 3. Migration Path
1. Create PeriodDefinition model
2. Update PeriodTemplate to use reverse relation
3. Move period generation logic to management command
4. Update views and serializers
5. Update tests

## Code Organization

### 1. Model Structure
```python
# schoolcalendar/models/period_definition.py
class PeriodDefinition(models.Model):
    # ... model fields ...

    def get_end_time(self):
        # ... time calculation ...

    def clean(self):
        # ... validation ...

    class Meta:
        ordering = ['template', 'start']
        constraints = [...]
```

### 2. Template Updates
```python
# schoolcalendar/models/period_template.py
class PeriodTemplate(MetadataModel):
    # Remove period count fields
    # Remove period_length
    # Keep metadata, versioning, etc.

    def get_periods(self):
        return self.perioddefinition_set.all()
```

## Testing Strategy

### 1. Model Tests
```python
def test_period_definition_validation(self):
    period = PeriodDefinition(
        template=template,
        number=1,
        length=45,
        start=time(8, 0),
        type='CLASS'
    )
    period.full_clean()  # Should validate

def test_overlapping_periods(self):
    # Test period overlap validation
```

### 2. Integration Tests
```python
def test_template_period_relationship(self):
    # Test template-period relationships
    # Test period ordering
    # Test time calculations
```

## Advantages of Early Implementation

1. Clean Design
- No legacy data constraints
- Can optimize from start
- Better testing coverage

2. Development Benefits
- Easier to implement now
- Can refine design freely
- No production constraints

3. Future-Proofing
- More flexible model
- Better extensibility
- Reduced technical debt

## Next Steps

1. Create feature branch
2. Implement PeriodDefinition model
3. Update PeriodTemplate
4. Add tests
5. Update related code
6. Review and refine

## Recommendation

Strongly recommend proceeding with this change now during local development because:
1. Current implementation has clear limitations
2. Proposed model is cleaner and more flexible
3. No production data/users to consider
4. Can implement and test thoroughly
5. Will reduce future technical debt

The 2-3 day timeline is reasonable for local development implementation.
