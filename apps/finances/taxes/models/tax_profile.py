from django.db import models

class TaxProfile(models.Model):
    tax_name = models.CharField(max_length=50)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tax_name} ({self.percentage}%)"