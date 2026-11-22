from apps.catalogs.variants.models.variant_profile import CatalogVariantProfile

class VariantApplicationService:
    @staticmethod
    def get_all_variants():
        return CatalogVariantProfile.objects.all()

    @staticmethod
    def create_variant(validated_data):
        return CatalogVariantProfile.objects.create(**validated_data)