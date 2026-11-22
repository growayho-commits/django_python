from django.contrib import admin
from .models import CheckoutProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CheckoutProfile)
class CheckoutProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CheckoutProfile._meta.fields]
    search_fields = [f.name for f in CheckoutProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
