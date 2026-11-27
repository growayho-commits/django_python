from django.db import models


class AttributeProfile(models.Model):
    INPUT_TYPE_CHOICES = [
        ("string", "Text"),
        ("select", "Dropdown Options"),
        ("number", "Number / Measurement"),
        ("boolean", "Yes / No"),
        ("color", "Color Swatch"),
    ]

    name = models.CharField(max_length=255, unique=True)
    code = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(
        "categories.CategoryProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="attributes",
        help_text="Leave blank for global attributes applicable across all categories.",
    )
    data_type = models.CharField(max_length=50, default="string")
    input_type = models.CharField(max_length=30, choices=INPUT_TYPE_CHOICES, default="string")
    options = models.JSONField(default=list, blank=True, help_text="Predefined choices for select/color attributes.")
    unit = models.CharField(max_length=30, blank=True, default="", help_text="e.g., kg, cm, GB, W, ml")
    is_variant_axis = models.BooleanField(default=False, help_text="If True, can generate SKU variations.")
    is_filterable = models.BooleanField(default=True)
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.unit})" if self.unit else self.name
