from django.db import models
from apps.common.choices import CoverageScopeChoices


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LocationCoverageMixin(models.Model):
    coverage_scope = models.CharField(
        max_length=30,
        choices=CoverageScopeChoices.choices,
        default=CoverageScopeChoices.ALL_INDIA,
    )
    coverage_locations = models.JSONField(
        default=list,
        blank=True,
        help_text="List of pincodes, taluks, districts, or states covered.",
    )

    class Meta:
        abstract = True