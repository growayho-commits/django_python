from apps.catalogs.variants.models.variant_profile import VariantProfile

def get_active_variants():
    return VariantProfile.objects.filter(is_active=True)