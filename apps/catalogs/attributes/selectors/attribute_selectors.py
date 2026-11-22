from apps.catalogs.attributes.models.attribute_profile import AttributeProfile

def get_required_attributes():
    return AttributeProfile.objects.filter(is_required=True)