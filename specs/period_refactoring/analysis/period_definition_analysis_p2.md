# Period Definition Analysis - Page 2: Implementation Strategy

## Implementation Plan

### Database Layer

#### 1. New Model Creation
```python
# migrations.py
operations = [
    migrations.CreateModel(
        name='PeriodDefinition',
        fields=[
            ('id', models.AutoField(primary_key=True)),
            ('template', models.ForeignKey(
                'PeriodTemplate',
                on_delete=models.CASCADE
            )),
            ('number', models.IntegerField()),
            ('length', models.IntegerField(
                validators=[
                    MinValueValidator(30),
                    MaxValueValidator(120)
                ]
            )),
            ('start', models.TimeField()),
            ('type', models.CharField(max_length=10)),
            ('passing', models.IntegerField(
                validators=[
                    MinValueValidator(0),
                    MaxValueValidator(30)
                ]
            )),
            ('meta', models.JSONField(default=dict)),
        ],
    ),
    migrations.AddIndex(
        model_name='perioddefinition',
        index=models.Index(
            fields=['template', 'start'],
            name='period_template_start_idx'
        ),
    ),
]
```

#### 2. Index Strategy
- Template-Start composite index
- Period number index
- Type index for filtering

#### 3. Constraints
```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['template', 'number'],
            name='unique_period_per_template'
        ),
        models.CheckConstraint(
            check=models.Q(length__gte=30) & models.Q(length__lte=120),
            name='valid_period_length'
        ),
        models.CheckConstraint(
            check=models.Q(passing__gte=0) & models.Q(passing__lte=30),
            name='valid_passing_time'
        ),
    ]
```

### Code Updates

#### 1. Logic Migration
```python
class PeriodDefinition(models.Model):
    # ... fields ...

    def get_end_time(self):
        start_dt = datetime.datetime.combine(
            datetime.date.today(),
            self.start
        )
        return (start_dt + datetime.timedelta(
            minutes=self.length
        )).time()

    def get_next_start_time(self):
        end_dt = datetime.datetime.combine(
            datetime.date.today(),
            self.get_end_time()
        )
        return (end_dt + datetime.timedelta(
            minutes=self.passing
        )).time()

    def validate_overlap(self):
        overlapping = PeriodDefinition.objects.filter(
            template=self.template,
            start__lt=self.get_end_time(),
            end_time__gt=self.start
        ).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError('Period overlaps with existing periods')
```

#### 2. Reference Updates
```python
class PeriodTemplate(MetadataModel):
    # Remove period generation fields
    # Add relationship accessor
    
    def get_periods(self):
        return self.perioddefinition_set.all()

    def get_period(self, number):
        return self.perioddefinition_set.filter(
            number=number
        ).first()
```

#### 3. Validation Logic
```python
class PeriodDefinitionForm(forms.ModelForm):
    class Meta:
        model = PeriodDefinition
        fields = ['number', 'length', 'start', 'type', 'passing']

    def clean(self):
        cleaned_data = super().clean()
        if all(k in cleaned_data for k in ('start', 'length')):
            # Validate period times
            instance = self.instance or self._meta.model()
            for field, value in cleaned_data.items():
                setattr(instance, field, value)
            instance.validate_overlap()
        return cleaned_data
```

### Cache Strategy

#### 1. Cache Keys
```python
CACHE_KEYS = {
    'period_definition': 'period:template:{template_id}:number:{number}',
    'template_periods': 'template:{template_id}:periods',
    'daily_schedule': 'schedule:date:{date}:template:{template_id}'
}
```

#### 2. Caching Logic
```python
class PeriodDefinition(models.Model):
    def cache_key(self):
        return CACHE_KEYS['period_definition'].format(
            template_id=self.template_id,
            number=self.number
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Invalidate related caches
        cache.delete(self.cache_key())
        cache.delete(
            CACHE_KEYS['template_periods'].format(
                template_id=self.template_id
            )
        )
```

### Timezone Handling

#### 1. Time Storage
```python
class PeriodDefinition(models.Model):
    # Store times in UTC
    start = models.TimeField(db_index=True)

    def get_local_start(self, tz=None):
        if tz is None:
            tz = timezone.get_current_timezone()
        dt = datetime.datetime.combine(
            datetime.date.today(),
            self.start
        )
        return timezone.localtime(dt, tz).time()
```

[Continued in Page 3...]
