from django.contrib import admin
from .models import SpecificationProfile

# --- Auto-Generated Model Registrations ---
@admin.register(SpecificationProfile)
class SpecificationProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SpecificationProfile._meta.fields]
    search_fields = [f.name for f in SpecificationProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
