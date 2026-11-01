import uuid
from django.db import models

class CatalogStatusProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.OneToOneField('core_catalogs.CoreCatalog', on_delete=models.CASCADE, related_name='status_profile')
    lifecycle_state = models.CharField(max_length=50, default='DRAFT')
    verified_by_superuser_id = models.CharField(max_length=100, blank=True, null=True)
    approval_rejection_reason = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_status_profile'

    @classmethod
    def update_state(cls, catalog_obj, dto) -> 'CatalogStatusProfile':
        valid_states = ['DRAFT', 'SUBMITTED', 'PENDING_REVIEW', 'CYCLIC_RECONCILIATION', 'APPROVED', 'REJECTED', 'PUBLISHED', 'UNPUBLISHED']
        if dto.lifecycle_state not in valid_states:
            raise ValueError(f"Domain Rule Error: Invalid state '{dto.lifecycle_state}'.")
        obj, _ = cls.objects.update_or_create(
            catalog=catalog_obj,
            defaults={
                'lifecycle_state': dto.lifecycle_state,
                'verified_by_superuser_id': dto.verified_by_superuser_id,
                'approval_rejection_reason': dto.approval_rejection_reason
            }
        )
        return obj
