from django.contrib import admin
from .models import AnalyticsProfile

# --- Auto-Generated Model Registrations ---
@admin.register(AnalyticsProfile)
class AnalyticsProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in AnalyticsProfile._meta.fields]
    search_fields = [f.name for f in AnalyticsProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
