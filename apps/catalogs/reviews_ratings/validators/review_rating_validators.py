from rest_framework.serializers import ValidationError

def validate_rating_score(value):
    if value < 1 or value > 5:
        raise ValidationError("Rating score must be between 1 and 5.")
    return value