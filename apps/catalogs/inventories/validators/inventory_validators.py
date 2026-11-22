from rest_framework.serializers import ValidationError

def validate_stock_quantity(value):
    if value < 0:
        raise ValidationError("Stock quantity cannot be negative.")
    return value