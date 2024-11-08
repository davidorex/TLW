from django.urls import path
from . import views

app_name = 'schoolcalendar'

urlpatterns = [
    path('', views.CalendarView.as_view(), name='index'),
]
