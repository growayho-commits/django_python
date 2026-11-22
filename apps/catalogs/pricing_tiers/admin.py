from django.contrib import admin
from .models import PricingTierProfile

# --- Auto-Generated Model Registrations ---
@admin.register(PricingTierProfile)
class PricingTierProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PricingTierProfile._meta.fields]
    search_fields = [f.name for f in PricingTierProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
