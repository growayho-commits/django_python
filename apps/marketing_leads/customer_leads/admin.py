from django.contrib import admin
from .models import CustomerLeadProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CustomerLeadProfile)
class CustomerLeadProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CustomerLeadProfile._meta.fields]
    search_fields = [f.name for f in CustomerLeadProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
