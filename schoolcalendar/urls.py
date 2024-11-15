from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from rest_framework.routers import DefaultRouter
from .views import (
    TermViewSet, 
    SchoolYearViewSet, 
    PeriodTemplateViewSet, 
    DashboardView, 
    DashboardCalendarView
)

router = DefaultRouter()
router.register(r'terms', TermViewSet)
router.register(r'school-years', SchoolYearViewSet)
router.register(r'period-templates', PeriodTemplateViewSet)

app_name = 'schoolcalendar'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),  # Root shows dashboard
    path('api/', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/calendar/', DashboardCalendarView.as_view(), name='dashboard-calendar'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('prev_month/', DashboardCalendarView.as_view(), name='prev_month'),  # Add prev_month URL
    path('next_month/', DashboardCalendarView.as_view(), name='next_month'),  # Add next_month URL
    path('day_view/', DashboardCalendarView.as_view(), name='day_view'),  # Add day_view URL
    path('week_view/', DashboardCalendarView.as_view(), name='week_view'),  # Add week_view URL
    path('month_view/', DashboardCalendarView.as_view(), name='month_view'),  # Add month_view URL
]
