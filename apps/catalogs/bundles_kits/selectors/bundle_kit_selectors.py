from apps.catalogs.bundles_kits.models.bundle_kit_profile import BundleKitProfile

def get_active_bundles():
    return BundleKitProfile.objects.filter(is_active=True)