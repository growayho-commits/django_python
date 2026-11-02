from django.conf import settings
from django.db import models

class OrderProfile(models.Model):
    """வாடிக்கையாளர் ஆர்டர்கள் மற்றும் வர்த்தகப் பரிமாற்றங்களை நிர்வகிக்கப் பயன்படும் பிரதான மாடல்"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="வாடிக்கையாளர்")
    order_number = models.CharField(max_length=100, unique=True, verbose_name="ஆர்டர் எண்")
    status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='pending', verbose_name="ஆர்டர் நிலை")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="மொத்த தொகை")
    shipping_address = models.TextField(verbose_name="டெலிவரி முகவரி")
    billing_address = models.TextField(verbose_name="பில் முகவரி")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="உருவாக்கப்பட்ட தேதி")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="கடைசியாக மாற்றப்பட்ட தேதி")

    def __str__(self):
        return f"Order #{self.order_number} - {self.status}"


class OrderItem(models.Model):
    """ஆர்டரில் உள்ள இயந்திரங்கள் மற்றும் உதிரிப் பாகங்களின் விவரங்கள்"""
    order = models.ForeignKey(OrderProfile, on_delete=models.CASCADE, related_name='items', verbose_name="தொடர்புடைய ஆர்டர்")
    product_id = models.CharField(max_length=100, verbose_name="தயாரிப்பு / பாக எண் (SKU)")
    quantity = models.PositiveIntegerField(default=1, verbose_name="அளவு")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ஒற்றைப் பொருளின் விலை")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="துணை மொத்தம்")

    def __str__(self):
        return f"Order Item {self.product_id} (Qty: {self.quantity})"