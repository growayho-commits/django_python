import uuid
from django.db import models

class SpecificationsProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.OneToOneField('core_catalogs.CoreCatalog', on_delete=models.CASCADE, related_name='specifications')
    dimensions_lwh = models.CharField(max_length=100)
    weight_kg = models.FloatField(default=0.0)
    material_type = models.CharField(max_length=150)
    operating_voltage = models.CharField(max_length=100, blank=True, null=True)
    compatibility_details = models.TextField(blank=True, null=True)
    technical_spec_sheet = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_specifications_profile'

    @classmethod
    def save_specifications(cls, catalog_obj, dto) -> 'SpecificationsProfile':
        obj, _ = cls.objects.update_or_create(
            catalog=catalog_obj,
            defaults={
                'dimensions_lwh': dto.dimensions_lwh,
                'weight_kg': dto.weight_kg,
                'material_type': dto.material_type,
                'operating_voltage': dto.operating_voltage,
                'compatibility_details': dto.compatibility_details,
                'technical_spec_sheet': dto.technical_spec_sheet
            }
        )
        return obj
