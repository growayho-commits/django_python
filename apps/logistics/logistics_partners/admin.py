from django.contrib import admin
from .models import LogisticsPartnerProfile

# --- Auto-Generated Model Registrations ---
@admin.register(LogisticsPartnerProfile)
class LogisticsPartnerProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in LogisticsPartnerProfile._meta.fields]
    search_fields = [f.name for f in LogisticsPartnerProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
