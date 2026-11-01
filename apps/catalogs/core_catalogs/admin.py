# apps/catalogs/core_catalogs/admin.py
from django.contrib import admin
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

@admin.register(CoreCatalog)
class CoreCatalogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sku', 'is_active', 'created_at']
    search_fields = ['name', 'sku']
    list_filter = ['is_active', 'created_at']