from django.contrib import admin
from .models import IntegrationProfile

# --- Auto-Generated Model Registrations ---
@admin.register(IntegrationProfile)
class IntegrationProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in IntegrationProfile._meta.fields]
    search_fields = [f.name for f in IntegrationProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
