# apps/catalogs/variants/services/variant_service.py

from apps.catalogs.variants.models.variant_profile import CatalogVariantProfile

class CatalogVariantService:
    @staticmethod
    def create_variant(validated_data):
        """புதிய தயாரிப்பு வகையைச் சேர்க்க (Add Variant)"""
        return CatalogVariantProfile.objects.create(**validated_data)

    @staticmethod
    def update_variant(variant_id, validated_data):
        """தயாரிப்பு வகையின் விவரங்களைப் புதுப்பிக்க (Edit / Update)"""
        try:
            variant = CatalogVariantProfile.objects.get(id=variant_id)
            for key, value in validated_data.items():
                setattr(variant, key, value)
            variant.save()
            return variant
        except CatalogVariantProfile.DoesNotExist:
            raise ValueError("Catalog variant profile does not exist.")