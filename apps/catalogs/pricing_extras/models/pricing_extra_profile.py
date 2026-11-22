from django.db import models

class PricingExtraProfile(models.Model):
    extra_name = models.CharField(max_length=255, unique=True)
    extra_code = models.SlugField(max_length=255, unique=True)
    additional_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_mandatory = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'pricing_extras'
        db_table = 'pricing_extra_profile'

    def __str__(self):
        return f"{self.extra_name} (+{self.additional_fee})"