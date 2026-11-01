from apps.catalogs.pricing_tiers.models.pricing_profile import PricingProfile

class PricingApplicationService:
    @staticmethod
    def create_pricing_tier(validated_data):
        """புதிய விலை அடுக்கை உருவாக்க (Create Pricing Tier)"""
        return PricingProfile.objects.create(**validated_data)

    @staticmethod
    def update_pricing_tier(pricing_id, validated_data):
        """ஏற்கனவே உள்ள விலை அடுக்கைப் புதுப்பிக்க (Update Pricing Tier)"""
        try:
            tier = PricingProfile.objects.get(id=pricing_id)
            for key, value in validated_data.items():
                setattr(tier, key, value)
            tier.save()
            return tier
        except PricingProfile.DoesNotExist:
            raise ValueError("Pricing tier does not exist.")