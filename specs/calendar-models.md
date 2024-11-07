# Calendar Framework Models

## Core Principle
Date-based calculations over relationship traversal, with patterns defining structure.

## Primary Models

### AcademicYear
Purpose: Defines school year structure and boundaries
```python
- uuid: UUID primary key
- academic_year: str  # "2024-2025"
- start_date: date
- end_date: date
- structure: Enum[SEMESTER, TRIMESTER]
- calendar_pattern: JSON  # Default schedule patterns
- metadata: JSONField  # Config, holidays, etc.

Methods:
- get_term_boundaries() -> list[date]
- get_term_for_date(date) -> Term
- is_school_day(date) -> bool
```

### Term
Purpose: Auto-generated academic periods
```python
- uuid: UUID primary key
- year: FK(AcademicYear)
- term_type: Enum[SEMESTER, TRIMESTER]
- sequence: int  # 1, 2 for semesters
- start_date: date
- end_date: date

Methods:
- get_week_number(date) -> int
- get_quarter_dates() -> list[date]  # If semester
```

### SchedulePattern
Purpose: Defines repeatable day structures
```python
- uuid: UUID primary key
- name: str  # "Standard Day", "Early Dismissal"
- morning_periods: int
- afternoon_periods: int
- evening_periods: int
- period_length: interval
- passing_time: interval
- pattern_type: Enum[DEFAULT, EXAM, SPECIAL]
- period_times: JSON  # Computed period schedule
- metadata: JSON  # Additional config

Methods:
- generate_periods(date) -> list[Period]
```

### SchoolDay
Purpose: Date-based schedule assignment
```python
- date: date primary key
- pattern_override: FK(SchedulePattern, null=True)
- status: Enum[REGULAR, EXAM, HOLIDAY]
- metadata: JSON  # Day-specific notes

Methods:
- get_schedule() -> SchedulePattern
- get_periods() -> list[Period]
```

## Implementation Notes
1. Minimal relationships - use date-based lookups
2. Cached calculations where appropriate
3. Business logic in model methods
4. No separate Week model - calculate from dates
5. JSON fields for flexible configuration

## Usage Pattern
```python
# Example view logic
day = SchoolDay.objects.get(date=target_date)
schedule = day.get_schedule()
periods = schedule.generate_periods(target_date)
```
