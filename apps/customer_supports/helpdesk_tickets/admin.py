from django.contrib import admin
from .models import HelpdeskTicket

# --- Auto-Generated Model Registrations ---
@admin.register(HelpdeskTicket)
class HelpdeskTicketAdmin(admin.ModelAdmin):
    list_display = [f.name for f in HelpdeskTicket._meta.fields]
    search_fields = [f.name for f in HelpdeskTicket._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
