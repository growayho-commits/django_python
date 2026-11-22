from django.contrib import admin
from .models import ReturnRefundProfile

# --- Auto-Generated Model Registrations ---
@admin.register(ReturnRefundProfile)
class ReturnRefundProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ReturnRefundProfile._meta.fields]
    search_fields = [f.name for f in ReturnRefundProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
