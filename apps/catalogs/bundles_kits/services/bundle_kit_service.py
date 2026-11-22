from apps.catalogs.bundles_kits.models.bundle_kit_profile import BundleKitProfile

class BundleKitApplicationService:
    @staticmethod
    def get_all_bundles():
        return BundleKitProfile.objects.all()

    @staticmethod
    def create_bundle(validated_data):
        return BundleKitProfile.objects.create(**validated_data)