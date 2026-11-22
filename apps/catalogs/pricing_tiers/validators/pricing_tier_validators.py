from rest_framework.serializers import ValidationError

def validate_discount_percentage(value):
    if value < 0 or value > 100:
        raise ValidationError("Discount percentage must be between 0 and 100.")
    return value