# Period Template Optimization Report

## Date: 2024-02-15
## Version: 1.0
## Author: Project Development Team

### Overview
Proposed optimization of PeriodTemplate model to address performance and usability concerns for a stable, rarely-changing period configuration.

### Motivation
- 96% of days use the same period structure
- Minimize computational overhead
- Optimize for read-heavy, infrequently changing data

### Proposed Changes

#### 1. PeriodTemplate Model Modifications
File: `schoolcalendar/models/period_template.py`

```python
class PeriodTemplate(MetadataModel):
    # Existing fields...
    
    # New field to cache generated periods
    cached_periods = models.JSONField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Auto-generate and cache periods on save
        if not self.cached_periods:
            self.cached_periods = self.generate_periods()
        super().save(*args, **kwargs)
    
    def get_cached_periods(self):
        # Return pre-generated periods
        return self.cached_periods or self.generate_periods()

    class Meta:
        # Enhanced indexing
        indexes = [
            models.Index(fields=['effective_from', 'version']),
            models.Index(fields=['name', 'version']),
            models.Index(fields=['is_default']),
            models.Index(fields=['name', 'version', 'effective_from'])
        ]
```

#### 2. Caching Strategy Update
File: `schoolcalendar/models/period_template.py`

```python
def get_active_template(self, date):
    cache_key = f'template:date:{date}'
    cached_template = cache.get(cache_key)
    
    if cached_template:
        return cached_template
    
    template = (
        self.filter(effective_from__lte=date)
        .order_by('-effective_from', '-version')
        .first()
    )
    
    if template:
        # Extended cache duration - potentially months
        cache.set(cache_key, template, timeout=2592000)  # 30-day cache
    
    return template
```

### Affected Files and Required Updates

1. Serializers
File: `schoolcalendar/serializers.py`
- Update `PeriodTemplateSerializer` to handle `cached_periods`
```python
class PeriodTemplateSerializer(serializers.ModelSerializer):
    cached_periods = serializers.JSONField(read_only=True)
    
    class Meta:
        model = PeriodTemplate
        fields = [
            # Existing fields...
            'cached_periods'
        ]
```

2. Views
File: `schoolcalendar/views.py`
- Ensure views use `get_cached_periods()` method
```python
class PeriodTemplateViewSet(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Attach cached periods to response
        data = serializer.data
        data['periods'] = instance.get_cached_periods()
        
        return Response(data)
```

3. Frontend Components
File: `static/js/components/period_template_manager.html`
- Update template rendering to use cached periods
```javascript
function renderTemplates(templates) {
    const templateList = document.getElementById('templateList');
    templateList.innerHTML = templates.map(template => `
        <div class="template-card">
            <h3>${template.name}</h3>
            <div class="periods">
                ${template.cached_periods ? 
                    template.cached_periods.map(period => 
                        `<div>${period.type} Period ${period.number}: ${period.start_time} - ${period.end_time}</div>`
                    ).join('') : 
                    'No cached periods'}
            </div>
        </div>
    `).join('');
}
```

### Migration Considerations
- Create a new migration to add `cached_periods` field
- Existing templates will need to have periods generated on first save

### Performance Expectations
- Reduced database queries
- Faster template retrieval
- Minimal runtime period generation overhead

### Risks and Mitigations
- Ensure cache invalidation on template updates
- Implement periodic cache refresh mechanisms
- Monitor performance impact during testing

### Next Steps
1. Implement proposed changes
2. Create comprehensive test suite
3. Perform performance benchmarking
4. Validate with stakeholders

### Approval
- Development Lead: [Signature/Approval Pending]
- Performance Architect: [Signature/Approval Pending]
