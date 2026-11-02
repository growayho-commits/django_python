from django.db import models

class CoreCatalog(models.Model):
    """மெஷினரி மற்றும் முக்கிய தயாரிப்புகளுக்கான பிரதான மாடல்"""
    name = models.CharField(max_length=255, unique=True, verbose_name="பெயர் / இயந்திரத்தின் பெயர்")
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU / மாடல் எண்")
    brand = models.CharField(max_length=100, blank=True, null=True, verbose_name="பிராண்ட்")
    description = models.TextField(blank=True, null=True, verbose_name="விவரங்கள்")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="விலை")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="இருப்பு அளவு")
    is_active = models.BooleanField(default=True, verbose_name="செயலில் உள்ளதா?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"


class SparePart(models.Model):
    """இயந்திரங்களுக்கான உதிரிப் பாகங்கள் மற்றும் மாற்றுப் பாகங்களை நிர்வகிக்க"""
    machinery = models.ForeignKey(
        CoreCatalog, 
        on_delete=models.CASCADE, 
        related_name='spare_parts', 
        verbose_name="தொடர்புடைய இயந்திரம் (CoreCatalog)"
    )
    part_name = models.CharField(max_length=255, verbose_name="உதிரிப் பாகத்தின் பெயர்")
    part_number = models.CharField(max_length=100, unique=True, verbose_name="பாக எண்")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="பாகத்தின் விலை")
    is_available = models.BooleanField(default=True, verbose_name="கிடைக்குமா?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.part_name} - {self.part_number} (For: {self.machinery.name})"