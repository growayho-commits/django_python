from rest_framework.serializers import ValidationError

def validate_category_name(value):
    if len(value) < 2:
        raise ValidationError("Category name must be at least 2 characters long.")
    return value