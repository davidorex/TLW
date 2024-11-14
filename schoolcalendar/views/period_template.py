class PeriodTemplateListView(LoginRequiredMixin, ListView):
    template_name = 'schoolcalendar/views/period_template_list.html'

class PeriodTemplateDetailView(LoginRequiredMixin, DetailView):
    template_name = 'schoolcalendar/views/period_template_detail.html'

class PeriodTemplateCreateView(LoginRequiredMixin, CreateView):
    template_name = 'schoolcalendar/views/period_template_form.html'

class PeriodTemplateUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'schoolcalendar/views/period_template_form.html' 