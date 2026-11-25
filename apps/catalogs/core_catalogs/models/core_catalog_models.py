import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class CoreCatalogProfile(models.Model):
    class UnitChoices(models.TextChoices):
        PIECE = 'pc', 'Piece'
        UNIT = 'unit', 'Unit'
        BOX = 'box', 'Box'
        KG = 'kg', 'Kilogram'
        LITER = 'ltr', 'Liter'
        SET = 'set', 'Set'

    class DeliveryScopeChoices(models.TextChoices):
        PINCODE = 'pincode', 'Specific Pincode(s)'
        TALUK = 'taluk', 'Taluk Based'
        DISTRICT = 'district', 'Single District'
        MULTI_DISTRICT = 'multi_district', 'Multiple Districts'
        STATE = 'state', 'Single State'
        MULTI_STATE = 'multi_state', 'Multiple States'
        ALL_INDIA = 'all_india', 'All Over India'

    class ApprovalStatusChoices(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending Approval'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    class TradeChannelChoices(models.TextChoices):
        B2B = 'b2b', 'B2B Supply (Merchant / Wholesale)'
        B2C = 'b2c', 'B2C Retail (Seller / Direct)'
        BOTH = 'both', 'Both B2B & B2C'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_catalogues',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        'categories.CategoryProfile',
        on_delete=models.SET_NULL,
        related_name='catalogues',
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    brand_name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Tax & Unit Standards
    hsn_sac_code = models.CharField(max_length=20, blank=True, null=True)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    unit = models.CharField(
        max_length=50,
        choices=UnitChoices.choices,
        default=UnitChoices.UNIT,
        blank=True,
        null=True,
    )

    # Base Pricing & Order Limits
    mrp_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    base_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    min_order_quantity = models.PositiveIntegerField(default=1)
    max_order_quantity = models.PositiveIntegerField(blank=True, null=True)

    # Transport & Geographic Delivery Coverage
    transport_included = models.BooleanField(
        default=True,
        help_text="If False, display '+ Delivery Charges Extra' to buyers.",
    )
    delivery_scope = models.CharField(
        max_length=30,
        choices=DeliveryScopeChoices.choices,
        default=DeliveryScopeChoices.ALL_INDIA,
    )
    delivery_locations = models.JSONField(
        default=list,
        blank=True,
        help_text="List of pincodes, taluks, districts, or states covered by this catalogue.",
    )

    trade_channel = models.CharField(
        max_length=10,
        choices=TradeChannelChoices.choices,
        default=TradeChannelChoices.B2C,
    )
    approval_status = models.CharField(
        max_length=20,
        choices=ApprovalStatusChoices.choices,
        default=ApprovalStatusChoices.DRAFT,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)[:230] or 'catalogue'
            candidate = base_slug
            counter = 1
            while CoreCatalogProfile.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = candidate

        if not self.sku:
            self.sku = f"CAT-{uuid.uuid4().hex[:8].upper()}"

        super().save(*args, **kwargs)

    @property
    def delivery_charge_label(self) -> str:
        return "Transport Included" if self.transport_included else "+ Delivery Charges Extra"

    def __str__(self):
        return f"{self.name} ({self.sku or self.unit})"