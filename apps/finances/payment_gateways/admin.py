from django.contrib import admin
from .models import PaymentGatewayConfig

# --- Auto-Generated Model Registrations ---
@admin.register(PaymentGatewayConfig)
class PaymentGatewayConfigAdmin(admin.ModelAdmin):
    list_display = [f.name for f in PaymentGatewayConfig._meta.fields]
    search_fields = [f.name for f in PaymentGatewayConfig._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
