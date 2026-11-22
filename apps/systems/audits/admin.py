from django.contrib import admin
from .models import AuditLogProfile

# --- Auto-Generated Model Registrations ---
@admin.register(AuditLogProfile)
class AuditLogProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in AuditLogProfile._meta.fields]
    search_fields = [f.name for f in AuditLogProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
