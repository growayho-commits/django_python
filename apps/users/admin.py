from django.contrib import admin

# 1. Executives Admin & Model
from apps.users.executives.admin import ExecutiveAdmin
from apps.users.executives.models.executive_profile import ExecutiveProfile

# 2. Guests Admin & Models
from apps.users.guests.admin import (
    AddressAdmin,
    BusinessProfileAdmin,
    GuestInquiryAdmin,
    OTPVerificationAdmin,
)
from apps.users.guests.models.address_profile import Address
from apps.users.guests.models.business_profile import BusinessProfile
from apps.users.guests.models.guest_inquiry import GuestInquiry
from apps.users.guests.models.security_profile import OTPVerification

# 3. Members Admin & Model
from apps.users.members.admin import MemberAdmin
from apps.users.members.models.member_profile import MemberProfile

# 4. Merchant Admin & Model
from apps.users.merchant.admin import MerchantAdmin
from apps.users.merchant.models.merchant_profile import MerchantProfile

# 5. Sellers Admin & Model
from apps.users.sellers.admin import SellerAdmin
from apps.users.sellers.models.seller_profile import SellerProfile

# 6. Superusers Admin & Models
from apps.users.superusers.admin import RoleUpgradeRequestAdmin, RoleRequirementAdmin
from apps.users.superusers.models.role_request import RoleUpgradeRequest
from apps.users.superusers.models.role_requirement import RoleRequirement

# Registration (Include)
admin.site.register(ExecutiveProfile, ExecutiveAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(BusinessProfile, BusinessProfileAdmin)
admin.site.register(GuestInquiry, GuestInquiryAdmin)
admin.site.register(OTPVerification, OTPVerificationAdmin)
admin.site.register(MemberProfile, MemberAdmin)
admin.site.register(MerchantProfile, MerchantAdmin)
admin.site.register(SellerProfile, SellerAdmin)
admin.site.register(RoleUpgradeRequest, RoleUpgradeRequestAdmin)
admin.site.register(RoleRequirement, RoleRequirementAdmin)