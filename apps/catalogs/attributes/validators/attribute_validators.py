from rest_framework.serializers import ValidationError

def validate_attribute_code(value):
    if not value.islower():
        raise ValidationError("Attribute code must be in lowercase letters.")
    return value