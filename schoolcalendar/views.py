from django.views.generic import TemplateView
from rest_framework import viewsets
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Term, SchoolYear, PeriodTemplate
from .serializers import TermSerializer, SchoolYearSerializer, PeriodTemplateSerializer
from django.utils import timezone
from django.shortcuts import render
import calendar
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer

class SchoolYearViewSet(viewsets.ModelViewSet):
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearSerializer

class PeriodTemplateViewSet(viewsets.ModelViewSet):
    queryset = PeriodTemplate.objects.all()
    serializer_class = PeriodTemplateSerializer

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'schoolcalendar/views/dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context['current_month'] = today.strftime("%B")
        context['current_year'] = today.year
        
        # Add initial calendar data
        active_template = PeriodTemplate.objects.get_active_template(today)
        context['periods'] = active_template.generate_periods() if active_template else []
        return context

class DashboardCalendarView(DashboardView):
    template_name = 'schoolcalendar/views/dashboard/calendar.html'
    section_name = 'calendar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = self.section_name
        today = timezone.now().date()
        context['current_month'] = today.strftime("%B")
        context['current_year'] = today.year
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request'):
            # Logic to fetch and render calendar content
            today = timezone.now().date()
            active_template = PeriodTemplate.objects.get_active_template(today)
            periods = active_template.generate_periods() if active_template else []  # Changed from periods_today to periods
            return render(request, 'schoolcalendar/partials/calendar_content.html', {'periods': periods})  # Changed context variable name
        return super().get(request, *args, **kwargs)

    def prev_month(self, request, *args, **kwargs):
        # Logic to handle previous month navigation
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        active_template = PeriodTemplate.objects.get_active_template(last_day_of_previous_month)
        periods = active_template.generate_periods() if active_template else []
        logger.debug(f"Previous month periods: {periods}")
        return render(request, 'schoolcalendar/partials/calendar_content.html', {'periods': periods})

    def next_month(self, request, *args, **kwargs):
        # Logic to handle next month navigation
        today = timezone.now().date()
        next_month = today.replace(day=28) + timedelta(days=4)  # this will never fail
        first_day_of_next_month = next_month.replace(day=1)
        active_template = PeriodTemplate.objects.get_active_template(first_day_of_next_month)
        periods = active_template.generate_periods() if active_template else []
        logger.debug(f"Next month periods: {periods}")
        return render(request, 'schoolcalendar/partials/calendar_content.html', {'periods': periods})

    def day_view(self, request, *args, **kwargs):
        # Logic to handle day view
        today = timezone.now().date()
        active_template = PeriodTemplate.objects.get_active_template(today)
        periods = active_template.generate_periods() if active_template else []  # Changed from periods_today to periods
        return render(request, 'schoolcalendar/partials/periods_today.html', {'periods': periods})  # Changed context variable name

    def week_view(self, request, *args, **kwargs):
        # Logic to handle week view
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        periods = []
        for single_date in (start_of_week + timedelta(n) for n in range(7)):
            active_template = PeriodTemplate.objects.get_active_template(single_date)
            periods.extend(active_template.generate_periods() if active_template else [])
        logger.debug(f"Week view periods: {periods}")
        return render(request, 'schoolcalendar/partials/calendar_content.html', {'periods': periods})

    def month_view(self, request, *args, **kwargs):
        # Logic to handle month view
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = (first_day_of_month.replace(month=first_day_of_month.month % 12 + 1, day=1) - timedelta(days=1))
        periods = []
        for single_date in (first_day_of_month + timedelta(n) for n in range((last_day_of_month - first_day_of_month).days + 1)):
            active_template = PeriodTemplate.objects.get_active_template(single_date)
            periods.extend(active_template.generate_periods() if active_template else [])
        logger.debug(f"Month view periods: {periods}")
        return render(request, 'schoolcalendar/partials/calendar_content.html', {'periods': periods})

class IndexView(TemplateView):
    template_name = 'schoolcalendar/views/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        active_template = PeriodTemplate.objects.get_active_template(today)
        if active_template:
            periods = active_template.generate_periods()  # Changed from periods_today to periods
            context['periods'] = periods  # Changed context variable name
        else:
            context['periods'] = []  # Changed context variable name
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request'):
            today = timezone.now().date()
            active_template = PeriodTemplate.objects.get_active_template(today)
            periods = active_template.generate_periods() if active_template else []  # Changed from periods_today to periods
            return render(request, 'schoolcalendar/partials/periods_today.html', {'periods': periods})  # Changed context variable name
        return super().get(request, *args, **kwargs)
