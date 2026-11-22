from django.contrib import admin
from .models import TaxProfile

# --- Auto-Generated Model Registrations ---
@admin.register(TaxProfile)
class TaxProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TaxProfile._meta.fields]
    search_fields = [f.name for f in TaxProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
