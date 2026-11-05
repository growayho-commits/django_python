from django.contrib import admin
from apps.catalogs.core_catalogs.models import CoreCatalog

@admin.register(CoreCatalog)
class CoreCatalogAdmin(admin.ModelAdmin):
    list_display = ('title', 'sku', 'vendor', 'price', 'stock', 'visibility', 'is_active')
    list_filter = ('visibility', 'is_active', 'created_at')
    search_fields = ('title', 'sku', 'vendor__email')