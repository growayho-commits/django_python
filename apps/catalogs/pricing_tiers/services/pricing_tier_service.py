from apps.catalogs.pricing_tiers.models.pricing_tier_profile import PricingTierProfile

class PricingTierApplicationService:
    @staticmethod
    def get_all_tiers():
        return PricingTierProfile.objects.all()

    @staticmethod
    def create_tier(validated_data):
        return PricingTierProfile.objects.create(**validated_data)