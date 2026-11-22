from django.contrib import admin
from .models import PricingExtraProfile

# --- Auto-Generated Model Registrations ---
@admin.register(PricingExtraProfile)
class PricingExtraProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PricingExtraProfile._meta.fields]
    search_fields = [f.name for f in PricingExtraProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
