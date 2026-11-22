from rest_framework.serializers import ValidationError

def validate_filter_key(value):
    if not value.islower():
        raise ValidationError("Filter key must be in lowercase.")
    return value