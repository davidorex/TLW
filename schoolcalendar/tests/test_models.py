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

class TermModelTests(TestCase):
    def setUp(self):
        self.school_year = SchoolYearFactory(term_structure='SEMESTER')

    def test_term_creation_validation(self):
        """Test Term creation with various validation scenarios"""
        # Test valid term creation
        term = TermFactory(year=self.school_year)
        term.full_clean()
        self.assertTrue(isinstance(term, Term))

        # Test term type constraints
        with self.assertRaises(ValidationError):
            invalid_term = Term(
                year=self.school_year,
                term_type='INVALID',
                sequence=1,
                start_date=self.school_year.start_date,
                end_date=self.school_year.end_date
            )
            invalid_term.full_clean()

    def test_term_sequence_constraints(self):
        """Test sequence constraints for terms"""
        # First term
        term1 = TermFactory(year=self.school_year, sequence=1)
        
        # Second term with correct sequence
        term2 = TermFactory(year=self.school_year, sequence=2)
        
        # Attempt to create term with duplicate sequence should fail
        with self.assertRaises(IntegrityError):
            Term.objects.create(
                year=self.school_year,
                term_type='SEM1',
                sequence=1,
                start_date=self.school_year.start_date,
                end_date=self.school_year.end_date
            )

    def test_term_date_validation(self):
        """Test date range validation for terms"""
        # Term dates within school year
        term = TermFactory(year=self.school_year)
        self.assertTrue(self.school_year.start_date <= term.start_date)
        self.assertTrue(term.end_date <= self.school_year.end_date)

        # Invalid date range should raise validation error
        with self.assertRaises(ValidationError):
            invalid_term = Term(
                year=self.school_year,
                term_type='SEM1',
                sequence=1,
                start_date=self.school_year.end_date,
                end_date=self.school_year.start_date
            )
            invalid_term.full_clean()

    def test_quarter_generation(self):
        """Test automatic quarter generation for semester terms"""
        # Create a semester term
        term = TermFactory(year=self.school_year, with_quarters=True)
        
        # Verify quarters were created
        quarters = Quarter.objects.filter(term=term)
        self.assertEqual(quarters.count(), 2)
        
        # Verify quarter dates
        for quarter in quarters:
            self.assertTrue(term.start_date <= quarter.start_date)
            self.assertTrue(quarter.end_date <= term.end_date)

    def test_current_term_detection(self):
        """Test is_current property"""
        from django.utils import timezone
        
        # Create terms around current date
        past_term = TermFactory(
            year=self.school_year, 
            start_date=timezone.now().date() - timezone.timedelta(days=180),
            end_date=timezone.now().date() - timezone.timedelta(days=90)
        )
        
        current_term = TermFactory(
            year=self.school_year, 
            start_date=timezone.now().date() - timezone.timedelta(days=30),
            end_date=timezone.now().date() + timezone.timedelta(days=30)
        )
        
        future_term = TermFactory(
            year=self.school_year, 
            start_date=timezone.now().date() + timezone.timedelta(days=90),
            end_date=timezone.now().date() + timezone.timedelta(days=180)
        )
        
        self.assertFalse(past_term.is_current)
        self.assertTrue(current_term.is_current)
        self.assertFalse(future_term.is_current)

    def test_term_week_calculations(self):
        """Test week number and duration calculations"""
        term = TermFactory(year=self.school_year)
        
        # Test duration_weeks
        expected_weeks = (term.end_date - term.start_date).days // 7
        self.assertEqual(term.duration_weeks, expected_weeks)
        
        # Test get_week_number
        mid_date = term.start_date + timezone.timedelta(days=int(term.duration_weeks * 7 / 2))
        week_number = term.get_week_number(mid_date)
        self.assertTrue(1 <= week_number <= term.duration_weeks)

    def test_term_metadata(self):
        """Test metadata schema and storage"""
        term = TermFactory(year=self.school_year)
        
        # Add metadata
        term.metadata = {
            "academic_weeks": [
                {
                    "week_number": 1,
                    "start_date": str(term.start_date),
                    "end_date": str(term.start_date + timezone.timedelta(days=6))
                }
            ],
            "special_dates": [
                {
                    "date": str(term.start_date),
                    "description": "First day of term"
                }
            ]
        }
        term.save()
        
        # Retrieve and verify
        retrieved_term = Term.objects.get(pk=term.pk)
        self.assertEqual(
            retrieved_term.metadata['academic_weeks'][0]['week_number'], 
            1
        )
