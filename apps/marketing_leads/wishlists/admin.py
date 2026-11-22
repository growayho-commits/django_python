from django.contrib import admin
from .models import Wishlist

# --- Auto-Generated Model Registrations ---
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Wishlist._meta.fields]
    search_fields = [f.name for f in Wishlist._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]
