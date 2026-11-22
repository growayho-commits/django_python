from django.contrib import admin
from .models import CommissionProfile

# --- Auto-Generated Model Registrations ---
@admin.register(CommissionProfile)
class CommissionProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CommissionProfile._meta.fields]
    search_fields = [f.name for f in CommissionProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
