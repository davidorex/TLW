from django.views.generic import TemplateView

class CalendarView(TemplateView):
    template_name = 'schoolcalendar/views/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Placeholder for calendar context data
        context['calendar_version'] = '2.0'
        return context
