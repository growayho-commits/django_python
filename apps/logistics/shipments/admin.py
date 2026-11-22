from django.contrib import admin
from .models import ShipmentProfile

# --- Auto-Generated Model Registrations ---
@admin.register(ShipmentProfile)
class ShipmentProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ShipmentProfile._meta.fields]
    search_fields = [f.name for f in ShipmentProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
