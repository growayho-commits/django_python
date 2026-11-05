from django.contrib import admin
from .models.merchant_profile import MerchantProfile

@admin.register(MerchantProfile)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'business_name', 'created_at')
    search_fields = ('business_name', 'user__email')
    list_filter = ('created_at',)