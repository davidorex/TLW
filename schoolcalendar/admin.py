from django.contrib import admin
from .models.term import Term
from .models.quarter import Quarter
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

@admin.register(Quarter)
class QuarterAdmin(admin.ModelAdmin):
    """
    Admin configuration for Quarter model
    """
    list_display = ('term', 'quarter_type', 'sequence', 'start_date', 'end_date')
    list_filter = ('term', 'quarter_type', 'sequence')
    search_fields = ('term__year__name', 'quarter_type')
    ordering = ('term', 'sequence')
    
    readonly_fields = ('metadata',)
    
    def get_readonly_fields(self, request, obj=None):
        """
        Make metadata read-only in admin interface
        """
        if obj:  # editing an existing object
            return self.readonly_fields + ('term',)
        return self.readonly_fields
