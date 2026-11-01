from django.db import models

class LogisticsReturnProfile(models.Model):
    RETURN_STATUS = [
        ('pickup_scheduled', 'Pickup Scheduled'),
        ('picked_up', 'Picked Up'),
        ('in_warehouse', 'Received at Warehouse'),
        ('inspecting', 'Inspecting'),
        ('completed', 'Completed'),
    ]

    return_request_id = models.CharField(max_length=100, unique=True)
    shipment = models.ForeignKey('shipments.ShipmentProfile', on_delete=models.CASCADE, related_name='return_shipments')
    status = models.CharField(max_length=30, choices=RETURN_STATUS, default='pickup_scheduled')
    pickup_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return Logistics #{self.return_request_id} - {self.status}"