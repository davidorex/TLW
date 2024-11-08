from django.contrib import admin
from ..models import (
    SchoolYear, Term, Quarter,
    PeriodTemplate, PeriodContent
)

admin.site.register(SchoolYear)
admin.site.register(Term)
admin.site.register(Quarter)
admin.site.register(PeriodTemplate)
admin.site.register(PeriodContent)

# Custom admin site configuration
admin.site.site_header = 'School Calendar Administration'
admin.site.site_title = 'School Calendar'
admin.site.index_title = 'Calendar Management'
