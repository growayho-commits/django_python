from apps.users.sellers.models import SellerProfile

class SellerService:
    @staticmethod
    def create_seller_profile(user, validated_data):
        profile, created = SellerProfile.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        return profile

    @staticmethod
    def verify_seller(seller_id):
        try:
            seller = SellerProfile.objects.get(id=seller_id)
            seller.is_verified = True
            seller.save()
            return seller
        except SellerProfile.DoesNotExist:
            raise ValueError("Seller profile does not exist.")