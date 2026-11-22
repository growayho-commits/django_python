from django.contrib import admin
from .models import SearchLog

# --- Auto-Generated Model Registrations ---
@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SearchLog._meta.fields]
    search_fields = [f.name for f in SearchLog._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
