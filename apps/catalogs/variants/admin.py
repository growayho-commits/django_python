# apps/catalogs/variants/admin.py
from django.contrib import admin
from apps.catalogs.variants.models.variant_profile import CatalogVariantProfile

@admin.register(CatalogVariantProfile)
class CatalogVariantProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'catalog', 'variant_name', 'sku', 'stock_quantity', 'is_active']
    search_fields = ['variant_name', 'sku']
    list_filter = ['is_active']