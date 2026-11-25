from django.core.exceptions import ValidationError
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile


def validate_unique_catalogue_name(name: str, instance=None) -> str:
    """Ensure every catalogue name is non-empty and unique (case-insensitive)."""
    cleaned_name = " ".join((name or "").split()).strip()
    if not cleaned_name:
        raise ValidationError("Catalogue name is required.")

    qs = CoreCatalogProfile.objects.filter(name__iexact=cleaned_name)
    if instance is not None and getattr(instance, "pk", None):
        qs = qs.exclude(pk=instance.pk)

    if qs.exists():
        raise ValidationError("A catalogue with this name already exists.")

    return cleaned_name