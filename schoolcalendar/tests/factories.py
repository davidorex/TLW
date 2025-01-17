import factory
from django.utils import timezone
from ..models import SchoolYear, Term, Quarter, PeriodTemplate, PeriodContent

class SchoolYearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolYear

    name = factory.Sequence(lambda n: f'School Year {n}')
    start_date = factory.LazyFunction(timezone.now().date)
    end_date = factory.LazyFunction(lambda: timezone.now().date() + timezone.timedelta(days=365))
    term_type = factory.Iterator(['SEMESTER', 'TRIMESTER'])

class TermFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Term
    
    year = factory.SubFactory(SchoolYearFactory)
    
    sequence = factory.Sequence(lambda n: n + 1)
    
    term_type = factory.LazyAttribute(
        lambda o: f"{'SEM' if o.year.term_type == 'SEMESTER' else 'TRI'}{o.sequence}"
    )
    
    start_date = factory.LazyAttribute(
        lambda obj: obj.year.start_date + timezone.timedelta(
            days=int((obj.sequence - 1) * (365 / (3 if obj.year.term_type == 'TRIMESTER' else 2)))
        )
    )
    
    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + timezone.timedelta(
            days=int(365 / (3 if obj.year.term_type == 'TRIMESTER' else 2)) - 1
        )
    )

    @factory.post_generation
    def with_quarters(obj, create, extracted, **kwargs):
        """
        Ensures quarters exist for semesters.
        Usage: TermFactory(with_quarters=True)
        """
        if create and extracted and obj.term_type.startswith('SEM'):
            QuarterFactory(term=obj, sequence=1)
            QuarterFactory(term=obj, sequence=2)

class QuarterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quarter

    term = factory.SubFactory(TermFactory)
    
    sequence = factory.Sequence(lambda n: 1 if n % 2 == 0 else 2)
    
    quarter_type = factory.LazyAttribute(
        lambda obj: f'Q{obj.sequence}'
    )
    
    start_date = factory.LazyAttribute(
        lambda obj: obj.term.start_date + timezone.timedelta(
            days=int((obj.sequence - 1) * (obj.term.end_date - obj.term.start_date).days / 2)
        )
    )
    
    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + timezone.timedelta(
            days=int((obj.term.end_date - obj.term.start_date).days / 2) - 1
        )
    )

    @factory.post_generation
    def with_metadata(obj, create, extracted, **kwargs):
        """
        Adds sample metadata to the quarter.
        Usage: QuarterFactory(with_metadata=True)
        """
        if create and extracted:
            obj.metadata = {
                "reporting_dates": {
                    "grades_due": str(obj.end_date),
                    "reports_published": str(obj.end_date + timezone.timedelta(days=7)),
                    "parent_meetings": {
                        "start": str(obj.end_date + timezone.timedelta(days=10)),
                        "end": str(obj.end_date + timezone.timedelta(days=14))
                    }
                },
                "assessment_weeks": [
                    {"week_number": 1, "type": "formative"},
                    {"week_number": 4, "type": "summative"}
                ]
            }
            obj.save()

class PeriodTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PeriodTemplate

    name = factory.Sequence(lambda n: f'Period Template {n}')
    
    schedule_type = factory.Iterator(['STD', 'EXT', 'RED', 'MOD'])
    
    effective_from = factory.LazyFunction(timezone.now().date)
    
    morning_periods = factory.Sequence(lambda n: (n % 6) + 1)
    
    afternoon_periods = factory.Sequence(lambda n: (n % 6) + 1)
    
    evening_periods = factory.Sequence(lambda n: (n % 4))
    
    period_length = factory.Sequence(lambda n: 45 + (n % 3) * 15)
    
    passing_time = factory.Sequence(lambda n: 5 + (n % 6))
    
    first_period = factory.LazyFunction(lambda: timezone.now().time().replace(hour=8, minute=0))
    
    version = 1  # Fixed version number instead of sequence

    @factory.post_generation
    def with_periods(obj, create, extracted, **kwargs):
        """
        Generates periods for the template.
        Usage: PeriodTemplateFactory(with_periods=True)
        """
        if create and extracted:
            periods = obj.generate_periods()
            # You could do additional processing with periods here if needed

class PeriodContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PeriodContent

    period_template = factory.SubFactory(PeriodTemplateFactory)
    content_type = factory.Faker('word')
    content_id = factory.Sequence(lambda n: n)
    start_time = factory.LazyFunction(timezone.now)
    end_time = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(hours=1))
