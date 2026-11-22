from rest_framework.serializers import ValidationError

def validate_media_url(value):
    if not value.startswith("http"):
        raise ValidationError("Media URL must be a valid HTTP/HTTPS link.")
    return value