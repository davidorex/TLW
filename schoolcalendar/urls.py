from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TermViewSet, SchoolYearViewSet, PeriodTemplateViewSet

router = DefaultRouter()
router.register(r'terms', TermViewSet)
router.register(r'school-years', SchoolYearViewSet)
router.register(r'period-templates', PeriodTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
