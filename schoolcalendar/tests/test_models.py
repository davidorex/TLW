from django.test import TestCase
from schoolcalendar.models.school_year import SchoolYear
from schoolcalendar.models.term import Term
from schoolcalendar.models.quarter import Quarter
from schoolcalendar.models.period_template import PeriodTemplate
from schoolcalendar.models.period_content import PeriodContent
from django.utils import timezone
from datetime import timedelta

class SchoolCalendarModelTests(TestCase):
    def setUp(self):
        # Create a sample school year
        self.school_year = SchoolYear.objects.create(
            name='2023-2024',
            start_date=timezone.now().date(),
            end_date=(timezone.now().date() + timedelta(days=365))
        )

    def test_school_year_creation(self):
        """Test SchoolYear model creation"""
        self.assertTrue(isinstance(self.school_year, SchoolYear))
        self.assertEqual(self.school_year.__str__(), self.school_year.name)

    def test_term_creation(self):
        """Test Term model creation and relationship with SchoolYear"""
        term = Term.objects.create(
            name='Fall Term',
            school_year=self.school_year,
            start_date=self.school_year.start_date,
            end_date=(self.school_year.start_date + timedelta(days=120))
        )
        self.assertTrue(isinstance(term, Term))
        self.assertEqual(term.school_year, self.school_year)

    def test_quarter_creation(self):
        """Test Quarter model creation and relationship with Term"""
        term = Term.objects.create(
            name='Fall Term',
            school_year=self.school_year,
            start_date=self.school_year.start_date,
            end_date=(self.school_year.start_date + timedelta(days=120))
        )
        quarter = Quarter.objects.create(
            name='First Quarter',
            term=term,
            start_date=term.start_date,
            end_date=(term.start_date + timedelta(days=60))
        )
        self.assertTrue(isinstance(quarter, Quarter))
        self.assertEqual(quarter.term, term)
