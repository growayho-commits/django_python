from django.contrib import admin
from .models import MerchantProfile

# --- Auto-Generated Model Registrations ---
@admin.register(MerchantProfile)
class MerchantProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MerchantProfile._meta.fields]
    search_fields = [f.name for f in MerchantProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
