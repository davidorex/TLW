from django.contrib import admin
from .models.term import Term
from .models.school_year import SchoolYear

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    """
    Admin configuration for Term model
    """
    list_display = ('year', 'term_type', 'sequence', 'start_date', 'end_date')
    list_filter = ('year', 'term_type')
    search_fields = ('year__name', 'term_type')
    ordering = ('year', 'sequence')
