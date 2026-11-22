from rest_framework.serializers import ValidationError

def validate_specification_value(value):
    if not value.strip():
        raise ValidationError("Specification value cannot be empty.")
    return value