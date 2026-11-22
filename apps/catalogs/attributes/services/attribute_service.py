from apps.catalogs.attributes.models.attribute_profile import AttributeProfile

class AttributeApplicationService:
    @staticmethod
    def get_all_attributes():
        return AttributeProfile.objects.all()

    @staticmethod
    def create_attribute(validated_data):
        return AttributeProfile.objects.create(**validated_data)