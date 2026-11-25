from django.conf import settings
from django.db import models


class TaxProfile(models.Model):
    tax_name = models.CharField(max_length=50)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tax_name} ({self.percentage}%)"


class InHouseGSTInvoice(models.Model):
    INVOICE_TYPE_CHOICES = [
        ('b2b_merchant_to_seller', 'Merchant -> Seller (B2B GST Invoice)'),
        ('b2c_seller_to_buyer', 'Seller -> Buyer (B2C GST Invoice)'),
        ('platform_commission', 'Platform Commission GST Invoice'),
    ]

    invoice_number = models.CharField(max_length=80, unique=True)
    invoice_type = models.CharField(max_length=40, choices=INVOICE_TYPE_CHOICES)
    order = models.ForeignKey(
        'orders.OrderProfile',
        on_delete=models.CASCADE,
        related_name='gst_invoices',
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='issued_gst_invoices',
        null=True,
        blank=True,
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='received_gst_invoices',
        null=True,
        blank=True,
    )
    seller_gstin = models.CharField(max_length=20, blank=True, default='UNREGISTERED')
    buyer_gstin = models.CharField(max_length=20, blank=True, default='UNREGISTERED')
    place_of_supply = models.CharField(max_length=100, default='Tamil Nadu')
    taxable_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    cgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sgst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    igst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_number} ({self.get_invoice_type_display()})"