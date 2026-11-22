from apps.catalogs.specifications.models.specification_profile import SpecificationProfile

class SpecificationApplicationService:
    @staticmethod
    def get_all_specifications():
        return SpecificationProfile.objects.all()

    @staticmethod
    def create_specification(validated_data):
        return SpecificationProfile.objects.create(**validated_data)