from rest_framework.serializers import ValidationError

def validate_variant_sku(value):
    if not value.strip():
        raise ValidationError("Variant SKU cannot be empty.")
    return value