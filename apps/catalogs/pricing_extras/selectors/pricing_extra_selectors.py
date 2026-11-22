from apps.catalogs.pricing_extras.models.pricing_extra_profile import PricingExtraProfile

def get_mandatory_extras():
    return PricingExtraProfile.objects.filter(is_mandatory=True)