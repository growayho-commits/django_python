from django.contrib import admin
from .models import AttributeProfile

# --- Auto-Generated Model Registrations ---
@admin.register(AttributeProfile)
class AttributeProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in AttributeProfile._meta.fields]
    search_fields = [f.name for f in AttributeProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
