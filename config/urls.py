from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from schoolcalendar.views import DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(DashboardView.as_view(), login_url='login'), name='index'),  # Redirect to dashboard if logged in
    path('calendar/', include('schoolcalendar.urls')),  # School calendar app
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += i18n_patterns(
    path('set_language/', include('django.conf.urls.i18n')),
)
