from django.db import models

class WarehouseTransferProfile(models.Model):
    TRANSFER_STATUS = [
        ('initiated', 'Initiated'),
        ('in_transit', 'In Transit'),
        ('received', 'Received'),
    ]

    transfer_reference = models.CharField(max_length=100, unique=True)
    source_warehouse = models.CharField(max_length=100)
    destination_warehouse = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=TRANSFER_STATUS, default='initiated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transfer #{self.transfer_reference} ({self.source_warehouse} to {self.destination_warehouse})"