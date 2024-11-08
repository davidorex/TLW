from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.utils import IntegrityError

from schoolcalendar.models.school_year import SchoolYear
from schoolcalendar.models.term import Term
from schoolcalendar.models.quarter import Quarter

from schoolcalendar.tests.factories import (
    SchoolYearFactory, 
    TermFactory, 
    QuarterFactory
)

class QuarterModelTests(TestCase):
    def setUp(self):
        # Create a semester school year and term for testing
        self.school_year = SchoolYearFactory(term_structure='SEMESTER')
        self.term = TermFactory(year=self.school_year, term_type='SEM1')

    def test_quarter_creation_validation(self):
        """
        Test Quarter creation with various validation scenarios
        """
        # Valid quarter creation
        quarter = QuarterFactory(term=self.term)
        quarter.full_clean()
        self.assertTrue(isinstance(quarter, Quarter))

        # Attempt to create quarter for non-semester term should fail
        non_semester_term = TermFactory(year=self.school_year, term_type='TRI1')
        with self.assertRaises(ValidationError):
            Quarter.objects.create(
                term=non_semester_term,
                quarter_type='Q1',
                sequence=1,
                start_date=non_semester_term.start_date,
                end_date=non_semester_term.end_date
            )

    def test_quarter_sequence_constraints(self):
        """
        Test sequence constraints for quarters
        """
        # First quarter
        quarter1 = QuarterFactory(term=self.term, sequence=1)
        
        # Second quarter
        quarter2 = QuarterFactory(term=self.term, sequence=2)
        
        # Attempt to create third quarter should fail
        with self.assertRaises(ValidationError):
            Quarter.objects.create(
                term=self.term,
                quarter_type='Q3',
                sequence=3,
                start_date=self.term.start_date,
                end_date=self.term.end_date
            )

    def test_quarter_date_validation(self):
        """
        Test date range validation for quarters
        """
        # Quarter dates within term
        quarter = QuarterFactory(term=self.term)
        self.assertTrue(self.term.start_date <= quarter.start_date)
        self.assertTrue(quarter.end_date <= self.term.end_date)

        # Invalid date range should raise validation error
        with self.assertRaises(ValidationError):
            Quarter.objects.create(
                term=self.term,
                quarter_type='Q1',
                sequence=1,
                start_date=self.term.end_date,
                end_date=self.term.start_date
            )

    def test_quarter_week_number(self):
        """
        Test get_week_number method
        """
        quarter = QuarterFactory(term=self.term)
        
        # Test week number calculation
        mid_date = quarter.start_date + timezone.timedelta(days=10)
        week_number = quarter.get_week_number(mid_date)
        
        self.assertIsNotNone(week_number)
        self.assertTrue(1 <= week_number <= (quarter.end_date - quarter.start_date).days // 7)

    def test_reporting_dates(self):
        """
        Test get_reporting_dates method
        """
        quarter = QuarterFactory(term=self.term)
        reporting_dates = quarter.get_reporting_dates()
        
        self.assertIn('grades_due', reporting_dates)
        self.assertIn('reports_published', reporting_dates)
        self.assertIn('parent_meetings', reporting_dates)
        
        # Verify dates are within expected ranges
        self.assertTrue(reporting_dates['grades_due'] <= quarter.end_date)
        self.assertTrue(reporting_dates['reports_published'] > quarter.end_date)

    def test_quarter_metadata(self):
        """
        Test metadata schema and storage
        """
        quarter = QuarterFactory(term=self.term, with_metadata=True)
        
        # Verify metadata structure
        self.assertIn('reporting_dates', quarter.metadata)
        self.assertIn('assessment_weeks', quarter.metadata)
        
        # Check specific metadata elements
        self.assertEqual(len(quarter.metadata['assessment_weeks']), 2)
        self.assertIn('week_number', quarter.metadata['assessment_weeks'][0])
        self.assertIn('type', quarter.metadata['assessment_weeks'][0])

    def test_quarter_caching(self):
        """
        Test caching mechanisms
        """
        from django.core.cache import cache
        
        quarter = QuarterFactory(term=self.term)
        
        # Test get_for_date caching
        Quarter.objects.get_for_date(quarter.start_date)
        cache_key = f'quarter:date:{quarter.start_date}'
        cached_quarter_id = cache.get(cache_key)
        
        self.assertEqual(cached_quarter_id, quarter.id)

    def test_unique_constraints(self):
        """
        Test unique constraints on quarters
        """
        # Create first quarter
        QuarterFactory(term=self.term, sequence=1, quarter_type='Q1')
        
        # Attempt to create duplicate should fail
        with self.assertRaises(IntegrityError):
            Quarter.objects.create(
                term=self.term,
                sequence=1,
                quarter_type='Q1',
                start_date=self.term.start_date,
                end_date=self.term.end_date
            )
