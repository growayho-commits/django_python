from django.conf import settings
from django.db import models


class PricingExtraProfile(models.Model):
    class CommissionMode(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage (%)'
        FLAT = 'flat', 'Flat Amount (₹)'

    catalogue = models.OneToOneField(
        'core_catalogs.CoreCatalogProfile',
        on_delete=models.CASCADE,
        related_name='commission_pricing',
        null=True,
        blank=True,
    )
    configured_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='configured_catalogue_commissions',
        null=True,
        blank=True,
    )

    # Superuser (Platform) Commission
    superuser_commission_mode = models.CharField(
        max_length=20,
        choices=CommissionMode.choices,
        default=CommissionMode.PERCENTAGE,
    )
    superuser_commission_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Executive Commission
    executive_commission_mode = models.CharField(
        max_length=20,
        choices=CommissionMode.choices,
        default=CommissionMode.PERCENTAGE,
    )
    executive_commission_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Seller Commission
    seller_commission_mode = models.CharField(
        max_length=20,
        choices=CommissionMode.choices,
        default=CommissionMode.PERCENTAGE,
    )
    seller_commission_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Optional Packaging / Handling / Estimated Delivery Extra Charge
    extra_handling_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estimated_delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Shown when catalogue transport_included is False.",
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        cat_name = self.catalogue.name if self.catalogue else "Unlinked Catalogue"
        return f"Commission & Pricing Rules - {cat_name}"