from django.contrib import admin
from .models import OrderProfile, OrderItem

# --- Auto-Generated Model Registrations ---
@admin.register(OrderProfile)
class OrderProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in OrderProfile._meta.fields]
    search_fields = [f.name for f in OrderProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [f.name for f in OrderItem._meta.fields]
    search_fields = [f.name for f in OrderItem._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
