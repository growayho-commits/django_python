from rest_framework.serializers import ValidationError

def validate_product_sku(value):
    if not value.strip():
        raise ValidationError("Product SKU cannot be empty for wishlist.")
    return value