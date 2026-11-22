from django.contrib import admin
from .models import CatalogVariantProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CatalogVariantProfile)
class CatalogVariantProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CatalogVariantProfile._meta.fields]
    search_fields = [f.name for f in CatalogVariantProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
