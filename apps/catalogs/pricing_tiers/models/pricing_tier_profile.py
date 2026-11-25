from django.db import models


class PricingTierProfile(models.Model):
    class AdjustmentType(models.TextChoices):
        FIXED_PRICE = 'fixed_price', 'Fixed Unit Price (₹)'
        PERCENTAGE_OFF = 'percentage_off', 'Percentage Discount (%)'
        FLAT_OFF = 'flat_off', 'Flat Amount Off (₹)'

    catalogue = models.ForeignKey(
        'core_catalogs.CoreCatalogProfile',
        on_delete=models.CASCADE,
        related_name='pricing_tiers',
        null=True,
        blank=True,
    )
    tier_name = models.CharField(max_length=120, default='Bulk Tier')
    min_quantity = models.PositiveIntegerField(default=1)
    max_quantity = models.PositiveIntegerField(blank=True, null=True)
    adjustment_type = models.CharField(
        max_length=20,
        choices=AdjustmentType.choices,
        default=AdjustmentType.FIXED_PRICE,
    )
    tier_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text="Unit price or discount (% / ₹) depending on adjustment_type.",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['min_quantity']

    def __str__(self):
        max_label = self.max_quantity if self.max_quantity else '+'
        return f"{self.tier_name} ({self.min_quantity}-{max_label}): {self.tier_value}"