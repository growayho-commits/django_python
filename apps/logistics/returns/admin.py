from django.contrib import admin
from .models import LogisticsReturnProfile

# --- Auto-Generated Model Registrations ---
@admin.register(LogisticsReturnProfile)
class LogisticsReturnProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in LogisticsReturnProfile._meta.fields]
    search_fields = [f.name for f in LogisticsReturnProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
