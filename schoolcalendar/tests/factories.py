import factory
from django.utils import timezone
from ..models import SchoolYear, Term, Quarter, PeriodTemplate, PeriodContent

class SchoolYearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolYear

    name = factory.Sequence(lambda n: f'School Year {n}')
    start_date = factory.LazyFunction(timezone.now().date)
    end_date = factory.LazyFunction(lambda: timezone.now().date() + timezone.timedelta(days=365))
    term_structure = factory.Iterator(['SEMESTER', 'TRIMESTER'])

class TermFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Term
    
    year = factory.SubFactory(SchoolYearFactory)
    
    sequence = factory.Sequence(lambda n: n + 1)
    
    term_type = factory.LazyAttribute(
        lambda o: f"{'SEM' if o.year.term_structure == 'SEMESTER' else 'TRI'}{o.sequence}"
    )
    
    start_date = factory.LazyAttribute(
        lambda obj: obj.year.start_date + timezone.timedelta(
            days=int((obj.sequence - 1) * (365 / (3 if obj.year.term_structure == 'TRIMESTER' else 2)))
        )
    )
    
    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + timezone.timedelta(
            days=int(365 / (3 if obj.year.term_structure == 'TRIMESTER' else 2)) - 1
        )
    )

    @factory.post_generation
    def with_quarters(obj, create, extracted, **kwargs):
        """
        Ensures quarters exist for semesters.
        Usage: TermFactory(with_quarters=True)
        """
        if create and extracted and obj.term_type.startswith('SEM'):
            from .quarter import Quarter
            from .factories import QuarterFactory
            
            # Create two quarters for a semester
            QuarterFactory(term=obj, sequence=1)
            QuarterFactory(term=obj, sequence=2)

class QuarterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quarter

    term = factory.SubFactory(TermFactory)
    sequence = factory.Sequence(lambda n: n + 1)
    
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

class PeriodTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PeriodTemplate

    name = factory.Sequence(lambda n: f'Period Template {n}')
    quarter = factory.SubFactory(QuarterFactory)
    duration = factory.LazyFunction(lambda: timezone.timedelta(days=30))
    description = factory.Faker('text')

class PeriodContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PeriodContent

    period_template = factory.SubFactory(PeriodTemplateFactory)
    content_type = factory.Faker('word')
    content_id = factory.Sequence(lambda n: n)
    start_time = factory.LazyFunction(timezone.now)
    end_time = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(hours=1))
