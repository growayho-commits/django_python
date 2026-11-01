# apps/catalogs/specifications/services/specifications_service.py

from apps.catalogs.specifications.models.specifications_profile import SpecificationsProfile

class SpecificationsApplicationService:
    @staticmethod
    def save_specification(validated_data):
        """ஸ்பெசிஃபிகேஷன் தகவல்களைச் சேமிக்க அல்லது புதுப்பிக்க"""
        spec_id = validated_data.get('id')
        if spec_id:
            spec = SpecificationsProfile.objects.get(id=spec_id)
            for key, value in validated_data.items():
                setattr(spec, key, value)
            spec.save()
            return spec
        else:
            return SpecificationsProfile.objects.create(**validated_data)