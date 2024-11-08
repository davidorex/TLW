import factory
from django.utils import timezone
from ..models import SchoolYear, Term, Quarter, PeriodTemplate, PeriodContent

class SchoolYearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolYear

    name = factory.Sequence(lambda n: f'School Year {n}')
    start_date = factory.LazyFunction(timezone.now().date)
    end_date = factory.LazyFunction(lambda: timezone.now().date() + timezone.timedelta(days=365))

class TermFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Term

    name = factory.Sequence(lambda n: f'Term {n}')
    school_year = factory.SubFactory(SchoolYearFactory)
    start_date = factory.LazyAttribute(lambda obj: obj.school_year.start_date)
    end_date = factory.LazyAttribute(lambda obj: obj.school_year.end_date)

class QuarterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quarter

    name = factory.Sequence(lambda n: f'Quarter {n}')
    term = factory.SubFactory(TermFactory)
    start_date = factory.LazyAttribute(lambda obj: obj.term.start_date)
    end_date = factory.LazyAttribute(lambda obj: obj.term.end_date)

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
