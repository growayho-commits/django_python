# apps/catalogs/bundles_kits/services/bundle_service.py

from apps.catalogs.bundles_kits.models.bundle_profile import BundleProfile

class BundleService:
    @staticmethod
    def create_bundle(validated_data):
        """புதிய தொகுப்புப் பொருளைச் சேர்க்க (Add Bundle)"""
        items = validated_data.pop('items', [])
        bundle = BundleProfile.objects.create(**validated_data)
        if items:
            bundle.items.set(items)
        return bundle

    @staticmethod
    def update_bundle(bundle_id, validated_data):
        """தொகுப்புப் பொருளின் விவரங்களைப் புதுப்பிக்க (Edit / Update)"""
        try:
            bundle = BundleProfile.objects.get(id=bundle_id)
            items = validated_data.pop('items', None)
            
            for key, value in validated_data.items():
                setattr(bundle, key, value)
            bundle.save()
            
            if items is not None:
                bundle.items.set(items)
                
            return bundle
        except BundleProfile.DoesNotExist:
            raise ValueError("Bundle profile does not exist.")