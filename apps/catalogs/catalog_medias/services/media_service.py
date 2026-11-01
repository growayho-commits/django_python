# apps/catalogs/catalog_medias/services/media_service.py

from apps.catalogs.catalog_medias.models.media_profile import CatalogMediaProfile

class CatalogMediaService:
    @staticmethod
    def create_media(validated_data):
        """புதிய மீடியா கோப்பைப் பதிவேற்றிச் சேர்க்க (Add Media)"""
        is_primary = validated_data.get('is_primary', False)
        catalog = validated_data.get('catalog')

        # ஒருவேளை இது முதன்மைப் படமாக இருந்தால், மற்ற படங்களின் is_primary-ஐ False ஆக மாற்றலாம்
        if is_primary and catalog:
            CatalogMediaProfile.objects.filter(catalog=catalog, is_primary=True).update(is_primary=False)

        return CatalogMediaProfile.objects.create(**validated_data)

    @staticmethod
    def update_media(media_id, validated_data):
        """மீடியா விவரங்களைப் புதுப்பிக்க (Edit / Update)"""
        try:
            media = CatalogMediaProfile.objects.get(id=media_id)
            is_primary = validated_data.get('is_primary', None)

            if is_primary is True:
                CatalogMediaProfile.objects.filter(catalog=media.catalog, is_primary=True).update(is_primary=False)

            for key, value in validated_data.items():
                setattr(media, key, value)
            media.save()
            return media
        except CatalogMediaProfile.DoesNotExist:
            raise ValueError("Media profile does not exist.")