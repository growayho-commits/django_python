import uuid
from django.db import models

class CoreCatalog(models.Model):
    """
    True DDD Aggregate Root for Global Hyper-Dynamic Catalog Engine.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_catalog_profile'
        verbose_name = 'Core Catalog'
        verbose_name_plural = 'Core Catalogs'

    def __str__(self):
        return f"{self.name} ({self.tenant_id})"

    @classmethod
    def create_catalog(cls, tenant_id: str, slug: str, name: str, description: str = None) -> 'CoreCatalog':
        """
        Domain Factory Method enforcing strict invariants.
        """
        if not tenant_id.strip():
            raise ValueError("Domain Invariant Violation: Tenant ID cannot be empty.")
        if not slug.strip():
            raise ValueError("Domain Invariant Violation: Catalog slug cannot be empty.")
        if not name.strip():
            raise ValueError("Domain Invariant Violation: Catalog name cannot be empty.")

        return cls(
            tenant_id=tenant_id.strip(),
            slug=slug.strip(),
            name=name.strip(),
            description=description,
            is_active=True
        )
