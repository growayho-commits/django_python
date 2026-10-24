from django.db import models


class ServiceCategory(models.Model):
    """
    சேவை வகைகள் - Google Business Categories & SAC Code அடிப்படையிலானது
    """
    name = models.CharField(max_length=255, verbose_name="Service Category Name")
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, 
        related_name='subcategories', verbose_name="Parent Service Category"
    )
    google_business_category = models.CharField(
        max_length=500, blank=True, null=True, verbose_name="Google Business Profile Category"
    )
    sac_code = models.CharField(max_length=20, verbose_name="SAC Code (GST)")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (SAC: {self.sac_code})"


class ServiceAttribute(models.Model):
    """
    சேவைக்கான தொழில்நுட்பப் பண்புத் தலைப்புகள் (Technical Specification Titles)
    """
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='service_attributes')
    title = models.CharField(max_length=100, verbose_name="Service Attribute Technical Title")

    def __str__(self):
        return f"{self.category.name} -> {self.title}"


class ServiceListing(models.Model):
    """
    முதன்மை சேவை வழங்குநர் பதிவு (Master Service Listing)
    """
    title = models.CharField(max_length=255, verbose_name="Service Title")
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ServiceVariationPlan(models.Model):
    """
    சேவை அளவுகள் மற்றும் கட்டணத் திட்டங்கள் (Service Scope / Plans)
    """
    service = models.ForeignKey(ServiceListing, on_delete=models.CASCADE, related_name='plans')
    plan_name = models.CharField(max_length=150, verbose_name="Plan Name / Scope")
    description = models.TextField(blank=True, null=True, verbose_name="Scope Details")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Service Fee / Plan Price")
    estimated_duration = models.CharField(max_length=50, blank=True, null=True, verbose_name="Duration (e.g., 2 Hours)")

    def __str__(self):
        return f"{self.service.title} - {self.plan_name} (₹{self.price})"