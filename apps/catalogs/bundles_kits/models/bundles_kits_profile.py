import uuid
from django.db import models

class BundlesKitsProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_bundle_catalog = models.ForeignKey('core_catalogs.CoreCatalog', on_delete=models.CASCADE, related_name='bundle_items')
    child_catalog = models.ForeignKey('core_catalogs.CoreCatalog', on_delete=models.CASCADE, related_name='part_of_bundles')
    quantity_in_bundle = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'catalog_bundles_kits_profile'

    @classmethod
    def add_to_bundle(cls, parent_catalog, child_catalog, quantity: int) -> 'BundlesKitsProfile':
        if quantity <= 0:
            raise ValueError("Domain Rule Error: Bundle item quantity must be greater than zero.")
        obj, _ = cls.objects.update_or_create(
            parent_bundle_catalog=parent_catalog,
            child_catalog=child_catalog,
            defaults={'quantity_in_bundle': quantity}
        )
        return obj
