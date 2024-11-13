from rest_framework import viewsets
from .models import Term, SchoolYear, PeriodTemplate
from .serializers import TermSerializer, SchoolYearSerializer, PeriodTemplateSerializer

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer

class SchoolYearViewSet(viewsets.ModelViewSet):
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearSerializer

class PeriodTemplateViewSet(viewsets.ModelViewSet):
    queryset = PeriodTemplate.objects.all()
    serializer_class = PeriodTemplateSerializer
