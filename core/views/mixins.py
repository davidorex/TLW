from django.contrib.auth.mixins import PermissionRequiredMixin as DjangoPermissionRequiredMixin

class PermissionRequiredMixin(DjangoPermissionRequiredMixin):
    """Base permission handling"""
    permission_required = None

    def has_permission(self):
        if self.permission_required is None:
            return True
        return super().has_permission()

class AuditableMixin:
    """Tracks model changes"""
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
