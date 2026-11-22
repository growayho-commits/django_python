from rest_framework.serializers import ValidationError

def validate_catalog_price(value):
    if value < 0:
        raise ValidationError("Base price cannot be negative.")
    return value