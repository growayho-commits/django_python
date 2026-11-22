from django.contrib import admin
from .models import SellerProfile

# --- Auto-Generated Model Registrations ---
@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SellerProfile._meta.fields]
    search_fields = [f.name for f in SellerProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
