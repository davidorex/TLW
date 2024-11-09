from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.cache import cache

from schoolcalendar.models.school_year import SchoolYear
from schoolcalendar.models.term import Term
from schoolcalendar.models.quarter import Quarter
from schoolcalendar.models.period_template import PeriodTemplate
from schoolcalendar.models.period_content import PeriodContent, get_default_template

from schoolcalendar.tests.factories import (
    SchoolYearFactory, 
    TermFactory, 
    QuarterFactory,
    PeriodTemplateFactory
)

class SchoolCalendarModelTests(TestCase):
    def setUp(self):
        # Create a sample school year
        self.school_year = SchoolYearFactory(term_type='SEMESTER')

    def test_school_year_creation(self):
        """Test SchoolYear model creation"""
        self.assertTrue(isinstance(self.school_year, SchoolYear))
        self.assertEqual(self.school_year.__str__(), self.school_year.name)

    def test_term_creation(self):
        """Test Term model creation and relationship with SchoolYear"""
        term = TermFactory(year=self.school_year)
        self.assertTrue(isinstance(term, Term))
        self.assertEqual(term.year, self.school_year)

    def test_quarter_creation(self):
        """Test Quarter model creation and relationship with Term"""
        term = TermFactory(year=self.school_year)
        quarter = QuarterFactory(term=term)
        self.assertTrue(isinstance(quarter, Quarter))
        self.assertEqual(quarter.term, term)

class PeriodTemplateModelTests(TestCase):
    def setUp(self):
        # Create a base period template for testing
        self.base_template = PeriodTemplateFactory()

    def test_period_template_creation(self):
        """
        Test basic PeriodTemplate creation
        """
        template = self.base_template
        self.assertTrue(isinstance(template, PeriodTemplate))
        self.assertEqual(template.version, 1)

    def test_period_generation(self):
        """
        Test generate_periods method
        """
        template = self.base_template
        periods = template.generate_periods()
        
        # Verify periods generated match template configuration
        self.assertEqual(
            len(periods), 
            template.morning_periods + template.afternoon_periods + template.evening_periods
        )
        
        # Check period numbering
        period_numbers = [period['number'] for period in periods]
        self.assertEqual(period_numbers, list(range(1, len(periods) + 1)))

    def test_period_times(self):
        """
        Test get_period_times method
        """
        template = self.base_template
        periods = template.generate_periods()
        
        # Test retrieving times for a specific period
        for period in periods:
            period_times = template.get_period_times(period['number'])
            self.assertEqual(period_times['start_time'], period['start_time'])
            self.assertEqual(period_times['end_time'], period['end_time'])

    def test_create_new_version(self):
        """
        Test creating a new version of a period template
        """
        template = self.base_template
        new_template = template.create_new_version()
        
        # Verify new version
        self.assertNotEqual(template.id, new_template.id)
        self.assertEqual(new_template.version, template.version + 1)
        self.assertEqual(new_template.name, template.name)

    def test_validation_period_counts(self):
        """
        Test validation of period counts
        """
        with self.assertRaises(ValidationError):
            invalid_template = PeriodTemplate(
                name='Invalid Template',
                morning_periods=0,
                afternoon_periods=0,
                evening_periods=0,
                period_length=45,
                passing_time=5,
                first_period=timezone.now().time(),
                effective_from=timezone.now().date()
            )
            invalid_template.full_clean()

    def test_validation_period_length(self):
        """
        Test validation of period length
        """
        with self.assertRaises(ValidationError):
            invalid_template = PeriodTemplate(
                name='Invalid Length Template',
                morning_periods=3,
                afternoon_periods=2,
                period_length=20,
                passing_time=5,
                first_period=timezone.now().time(),
                effective_from=timezone.now().date()
            )
            invalid_template.full_clean()

    def test_active_template_caching(self):
        """
        Test active template caching mechanism
        """
        template = self.base_template
        date = timezone.now().date()
        
        # First retrieval should query database
        active_template = PeriodTemplate.objects.get_active_template(date)
        self.assertEqual(active_template, template)
        
        # Verify cache was set
        cache_key = f'template:date:{date}'
        cached_template_id = cache.get(cache_key)
        self.assertEqual(cached_template_id, template.id)

        # Second retrieval should use cache
        cached_template = PeriodTemplate.objects.get_active_template(date)
        self.assertEqual(cached_template, template)

    def test_version_constraint(self):
        """
        Test version constraint when creating new templates
        """
        template = self.base_template
        
        # Create a template with the same name but lower version should fail
        with self.assertRaises(ValidationError):
            duplicate_version = PeriodTemplate(
                name=template.name,
                version=template.version,
                morning_periods=3,
                afternoon_periods=2,
                period_length=45,
                passing_time=5,
                first_period=timezone.now().time(),
                effective_from=timezone.now().date()
            )
            duplicate_version.full_clean()

    def test_default_template(self):
        """
        Test default template functionality
        """
        # Create a default template
        default_template = PeriodTemplateFactory(is_default=True)
        
        # Verify get_default returns the correct template
        self.assertEqual(PeriodTemplate.objects.get_default(), default_template)
        
        # Create another default template should update the default
        new_default = PeriodTemplateFactory(is_default=True)
        self.assertFalse(PeriodTemplate.objects.get(pk=default_template.pk).is_default)
        self.assertEqual(PeriodTemplate.objects.get_default(), new_default)

class PeriodContentModelTests(TestCase):
    def setUp(self):
        self.default_template = PeriodTemplateFactory(is_default=True)
        self.non_default_template = PeriodTemplateFactory(is_default=False)

    def test_get_default_template(self):
        """
        Test get_default_template function behavior
        """
        # Should return the default template's pk
        self.assertEqual(get_default_template(), self.default_template.pk)
        
        # After removing default flag, should return None
        self.default_template.is_default = False
        self.default_template.save()
        self.assertIsNone(get_default_template())

    def test_period_content_creation_with_default_template(self):
        """
        Test PeriodContent creation using default template
        """
        content = PeriodContent.objects.create(
            date=timezone.now().date(),
            period_number=1
        )
        self.assertEqual(content.template, self.default_template)

    def test_period_content_creation_without_default_template(self):
        """
        Test PeriodContent creation when no default template exists
        """
        # Remove default flag
        self.default_template.is_default = False
        self.default_template.save()
        
        content = PeriodContent.objects.create(
            date=timezone.now().date(),
            period_number=1
        )
        self.assertIsNone(content.template)

    def test_period_content_explicit_template(self):
        """
        Test PeriodContent creation with explicitly specified template
        """
        content = PeriodContent.objects.create(
            date=timezone.now().date(),
            period_number=1,
            template=self.non_default_template
        )
        self.assertEqual(content.template, self.non_default_template)
