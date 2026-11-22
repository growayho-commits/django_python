from apps.catalogs.pricing_tiers.models.pricing_tier_profile import PricingTierProfile

def get_active_pricing_tiers():
    return PricingTierProfile.objects.filter(is_active=True)