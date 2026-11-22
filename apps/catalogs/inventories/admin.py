from django.contrib import admin
from .models import InventoryProfile

# --- Auto-Generated Model Registrations ---
@admin.register(InventoryProfile)
class InventoryProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in InventoryProfile._meta.fields]
    search_fields = [f.name for f in InventoryProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
