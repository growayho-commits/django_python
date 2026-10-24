from apps.catalogs.bundles_kits.models.bundles_kits_profile import BundlesKitsProfile

class BundlesKitsSelector:
    @staticmethod
    def get_bundle_items(parent_catalog_id: str):
        return BundlesKitsProfile.objects.filter(parent_bundle_catalog_id=parent_catalog_id)
