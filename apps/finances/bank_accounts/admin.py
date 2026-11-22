from django.contrib import admin
from .models import BankAccountProfile

# --- Auto-Generated Model Registrations ---
@admin.register(BankAccountProfile)
class BankAccountProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in BankAccountProfile._meta.fields]
    search_fields = [f.name for f in BankAccountProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
