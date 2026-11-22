from rest_framework.serializers import ValidationError

def validate_status_code(value):
    if not value.islower():
        raise ValidationError("Status code must be in lowercase letters.")
    return value