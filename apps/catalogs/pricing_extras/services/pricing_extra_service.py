from apps.catalogs.pricing_extras.models.pricing_extra_profile import PricingExtraProfile

class PricingExtraApplicationService:
    @staticmethod
    def get_all_extras():
        return PricingExtraProfile.objects.all()

    @staticmethod
    def create_extra(validated_data):
        return PricingExtraProfile.objects.create(**validated_data)