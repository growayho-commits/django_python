from django.contrib import admin
from .models import FAQProfile

# --- Auto-Generated Model Registrations ---
@admin.register(FAQProfile)
class FAQProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in FAQProfile._meta.fields]
    search_fields = [f.name for f in FAQProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
