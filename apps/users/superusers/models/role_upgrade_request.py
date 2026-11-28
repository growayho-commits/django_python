from django.db import models
from django.conf import settings


SUB_ROLE_OPTIONS = {
    'merchant': [
        'Raw Material Supplier',
        'Manufacturer',
        'MSME (Micro, Small & Medium Enterprise)',
        'OEM / White-Label Manufacturer',
        'Brand Owner',
        'Importer / Exporter',
        'C&F / Super Stockist',
        'Distributor',
        'Wholesaler',
    ],
    'seller': [
        'Manufacturer (Direct B2C)',
        'MSME (Micro, Small & Medium Enterprise)',
        'Authorised Dealer',
        'Sub-Dealer / Franchisee',
        'Retailer / Shopkeeper',
        'Reseller / Social Seller',
        'Dropshipper',
        'D2C Brand',
    ],
    'executive': [
        'Broker / Commission Agent',
        'Sourcing / Buying Agent',
        'C&F / Warehouse Partner',
        'Logistics / 3PL Delivery Partner',
        'Field Inspection Executive',
        'Onboarding / Affiliate Partner',
        'Department Employee (Salaried)',
    ],
    'member': [
        'Individual Consumer',
        'Corporate / Institutional Buyer',
        'Service Seeker',
    ],
    'superuser': [
        'Platform Owner / Core Admin',
    ],
}


class RoleUpgradeRequest(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('seller', 'Seller'),
        ('merchant', 'Merchant'),
        ('executive', 'Executive'),
        ('superuser', 'Superuser'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='role_requests')
    requested_role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    sub_roles = models.JSONField(default=list, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_role_requests'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} -> {self.requested_role} ({self.status})"
