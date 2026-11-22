from django.contrib import admin
from .models import CartProfile, CartItem

# --- Auto-Generated Model Registrations ---
@admin.register(CartProfile)
class CartProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CartProfile._meta.fields]
    search_fields = [f.name for f in CartProfile._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CartItem._meta.fields]
    search_fields = [f.name for f in CartItem._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
