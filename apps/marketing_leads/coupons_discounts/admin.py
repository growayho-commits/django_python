from django.contrib import admin
from .models import CouponDiscountProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CouponDiscountProfile)
class CouponDiscountProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CouponDiscountProfile._meta.fields]
    search_fields = [f.name for f in CouponDiscountProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
