from rest_framework.serializers import ValidationError

def validate_additional_fee(value):
    if value < 0:
        raise ValidationError("Additional fee cannot be negative.")
    return value