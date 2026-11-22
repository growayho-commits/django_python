from django.contrib import admin
from .models import SearchFilterProfile

# --- Auto-Generated Model Registrations ---
@admin.register(SearchFilterProfile)
class SearchFilterProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SearchFilterProfile._meta.fields]
    search_fields = [f.name for f in SearchFilterProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
