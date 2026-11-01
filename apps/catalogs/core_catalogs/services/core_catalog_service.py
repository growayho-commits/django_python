# apps/catalogs/core_catalogs/services/core_catalog_service.py

from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CoreCatalogService:
    @staticmethod
    def create_catalog_item(validated_data):
        """புதிய கேட்டலாக் பொருளைச் சேர்க்க (Add)"""
        return CoreCatalog.objects.create(**validated_data)

    @staticmethod
    def update_catalog_item(catalog_id, validated_data):
        """ஏற்கனவே உள்ள கேட்டலாக் பொருளைப் புதுப்பிக்க (Edit / Update)"""
        try:
            item = CoreCatalog.objects.get(id=catalog_id)
            for key, value in validated_data.items():
                setattr(item, key, value)
            item.save()
            return item
        except CoreCatalog.DoesNotExist:
            raise ValueError("Catalog item does not exist.")