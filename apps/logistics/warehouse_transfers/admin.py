from django.contrib import admin
from .models import WarehouseTransferProfile

# --- Auto-Generated Model Registrations ---
@admin.register(WarehouseTransferProfile)
class WarehouseTransferProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WarehouseTransferProfile._meta.fields]
    search_fields = [f.name for f in WarehouseTransferProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
