from django.contrib import admin
from .models import CatalogMediaProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CatalogMediaProfile)
class CatalogMediaProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CatalogMediaProfile._meta.fields]
    search_fields = [f.name for f in CatalogMediaProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
