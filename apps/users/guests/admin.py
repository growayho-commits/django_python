from django.contrib import admin
from .models.address_profile import Address
from .models.business_profile import BusinessProfile
from .models.guest_inquiry import GuestInquiry
from .models.security_profile import OTPVerification

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'created_at')
    search_fields = ('city', 'user__email')

@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    # 'business_name'-க்கு பதிலாக மாடலில் உள்ள சரியான 'company_name' மற்றும் 'business_type' பயன்படுத்தப்பட்டுள்ளது[cite: 1]
    list_display = ('id', 'user', 'company_name', 'business_type', 'is_verified_business', 'created_at')
    search_fields = ('company_name', 'user__email', 'gstin_or_tax_id')
    list_filter = ('business_type', 'is_verified_business', 'created_at')

@admin.register(GuestInquiry)
class GuestInquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'subject', 'created_at')
    search_fields = ('email', 'subject')

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_verified', 'created_at')
    search_fields = ('user__email',)