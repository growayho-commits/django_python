from django.contrib import admin
from .models import CatalogStatusProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CatalogStatusProfile)
class CatalogStatusProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CatalogStatusProfile._meta.fields]
    search_fields = [f.name for f in CatalogStatusProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
