from django.contrib import admin
from .models import CoreCatalogProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CoreCatalogProfile)
class CoreCatalogProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CoreCatalogProfile._meta.fields]
    search_fields = [f.name for f in CoreCatalogProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
