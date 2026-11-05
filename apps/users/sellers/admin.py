from django.contrib import admin
from .models.seller_profile import SellerProfile

@admin.register(SellerProfile)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'store_name', 'created_at')
    search_fields = ('store_name', 'user__email')
    list_filter = ('created_at',)