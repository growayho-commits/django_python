from apps.users.merchant.models import MerchantProfile

class MerchantService:
    @staticmethod
    def create_merchant_profile(user, validated_data):
        profile, created = MerchantProfile.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        return profile

    @staticmethod
    def verify_merchant(merchant_id):
        try:
            merchant = MerchantProfile.objects.get(id=merchant_id)
            merchant.is_verified = True
            merchant.save()
            return merchant
        except MerchantProfile.DoesNotExist:
            raise ValueError("Merchant profile does not exist.")