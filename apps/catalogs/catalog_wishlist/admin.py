from django.contrib import admin
from .models import CatalogWishlistProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CatalogWishlistProfile)
class CatalogWishlistProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CatalogWishlistProfile._meta.fields]
    search_fields = [f.name for f in CatalogWishlistProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
