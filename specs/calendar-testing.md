# Calendar Testing Framework

## Model Constraints & Relationships

### AcademicYear
```python
class AcademicYear:
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gt=F('start_date')),
                name='academic_year_dates_ordered'
            ),
            models.CheckConstraint(
                check=Q(start_date__month__in=[7, 8, 9]),  # Common school year starts
                name='valid_academic_year_start'
            ),
            models.UniqueConstraint(
                fields=['academic_year'],
                name='unique_academic_year'
            )
        ]
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
        ]
```

### Term
```python
class Term:
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(end_date__gt=F('start_date')),
                name='term_dates_ordered'
            ),
            models.CheckConstraint(
                check=Q(sequence__in=[1, 2, 3]),  # 1-2 for semester, 1-3 for trimester
                name='valid_term_sequence'
            ),
            models.UniqueConstraint(
                fields=['year', 'sequence'],
                name='unique_term_sequence_per_year'
            )
        ]
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['year', 'sequence'])
        ]
```

### SchoolDay
```python
class SchoolDay:
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date'],
                name='unique_school_day'
            )
        ]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['status'])
        ]
```

## Test Factories

```python
import factory
from factory.django import DjangoModelFactory
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class AcademicYearFactory(DjangoModelFactory):
    class Meta:
        model = 'calendar.AcademicYear'

    academic_year = factory.Sequence(lambda n: f"202{n}-202{n+1}")
    start_date = factory.LazyFunction(
        lambda: date(2024, 8, 1)
    )
    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + relativedelta(months=10)
    )
    structure = 'SEMESTER'
    calendar_pattern = factory.Dict({
        'periods_per_day': 8,
        'period_length_minutes': 45,
        'passing_time_minutes': 5
    })
    metadata = factory.Dict({
        'holiday_dates': [],
        'exam_dates': []
    })

class TermFactory(DjangoModelFactory):
    class Meta:
        model = 'calendar.Term'

    year = factory.SubFactory(AcademicYearFactory)
    term_type = factory.LazyAttribute(
        lambda obj: obj.year.structure
    )
    sequence = factory.Sequence(lambda n: n + 1)
    start_date = factory.LazyAttribute(
        lambda obj: obj.year.start_date + relativedelta(months=(obj.sequence-1)*5)
    )
    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + relativedelta(months=5, days=-1)
    )

class SchedulePatternFactory(DjangoModelFactory):
    class Meta:
        model = 'calendar.SchedulePattern'

    name = factory.Sequence(lambda n: f"Schedule Pattern {n}")
    morning_periods = 4
    afternoon_periods = 4
    evening_periods = 0
    period_length = timedelta(minutes=45)
    passing_time = timedelta(minutes=5)
    pattern_type = 'DEFAULT'
    period_times = factory.LazyAttribute(
        lambda obj: {
            f"period_{i}": {
                "start": f"{8+i}:00",
                "end": f"{8+i}:45"
            } for i in range(obj.morning_periods + obj.afternoon_periods)
        }
    )

class SchoolDayFactory(DjangoModelFactory):
    class Meta:
        model = 'calendar.SchoolDay'

    date = factory.Sequence(
        lambda n: date(2024, 8, 1) + timedelta(days=n)
    )
    pattern_override = None
    status = 'REGULAR'
    metadata = factory.Dict({})
```

## Core Test Cases

```python
from django.test import TestCase
from datetime import date, timedelta

class CalendarModelTests(TestCase):
    def setUp(self):
        self.academic_year = AcademicYearFactory()
        self.term = TermFactory(year=self.academic_year)
        self.pattern = SchedulePatternFactory()
        self.school_day = SchoolDayFactory(
            date=self.term.start_date
        )

    def test_academic_year_boundaries(self):
        """Test academic year date validation and term generation"""
        self.assertTrue(self.academic_year.end_date > self.academic_year.start_date)
        self.assertEqual(
            len(self.academic_year.get_term_boundaries()),
            2 if self.academic_year.structure == 'SEMESTER' else 3
        )

    def test_term_week_calculation(self):
        """Test week number calculations within term"""
        mid_term_date = self.term.start_date + timedelta(weeks=6)
        self.assertEqual(self.term.get_week_number(mid_term_date), 7)

    def test_schedule_pattern_generation(self):
        """Test period generation from pattern"""
        periods = self.pattern.generate_periods(date.today())
        self.assertEqual(
            len(periods),
            self.pattern.morning_periods + self.pattern.afternoon_periods
        )

    def test_school_day_schedule_resolution(self):
        """Test schedule pattern resolution for school day"""
        schedule = self.school_day.get_schedule()
        self.assertIsNotNone(schedule)
        periods = self.school_day.get_periods()
        self.assertTrue(len(periods) > 0)
```

## Integration Tests

```python
class CalendarIntegrationTests(TestCase):
    def setUp(self):
        self.academic_year = AcademicYearFactory()
        TermFactory.create_batch(
            2 if self.academic_year.structure == 'SEMESTER' else 3,
            year=self.academic_year
        )
        self.default_pattern = SchedulePatternFactory()
        self.exam_pattern = SchedulePatternFactory(
            pattern_type='EXAM',
            morning_periods=3,
            afternoon_periods=2
        )

    def test_full_year_generation(self):
        """Test complete academic year setup"""
        current_date = self.academic_year.start_date
        while current_date <= self.academic_year.end_date:
            if self.academic_year.is_school_day(current_date):
                day = SchoolDayFactory(date=current_date)
                self.assertIsNotNone(day.get_schedule())
            current_date += timedelta(days=1)

    def test_term_transitions(self):
        """Test proper handling of term boundaries"""
        for term in self.academic_year.term_set.all():
            self.assertTrue(
                self.academic_year.get_term_for_date(term.start_date) == term
            )
```

Would you like me to expand on any of these aspects or move on to view specifications next?