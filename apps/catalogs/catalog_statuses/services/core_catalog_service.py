from django.db import transaction
from apps.catalog.core_catalog.models.core_catalog_profile import CoreCatalog, CatalogType

class CoreCatalogService:
    """
    Write operations and business logic handlers for Core Catalog[cite: 1].
    """
    @staticmethod
    @transaction.atomic
    def create_catalog(validated_data: dict) -> CoreCatalog:
        # Automatic determination of Catalog Type based on HSN/SAC prefix[cite: 1]
        code = validated_data.get('hsn_or_sac_code', '')
        if code.startswith('99'):
            catalog_type = CatalogType.SERVICE
        else:
            catalog_type = CatalogType.GOODS

        validated_data['catalog_type'] = catalog_type
        
        catalog = CoreCatalog.objects.create(**validated_data)
        return catalog

    @staticmethod
    @transaction.atomic
    def update_catalog(catalog_id: str, validated_data: dict) -> CoreCatalog:
        catalog = CoreCatalog.objects.get(id=catalog_id)
        for attr, value in validated_data.items():
            setattr(catalog, attr, value)
        catalog.save()
        return catalog
[cite: 1]