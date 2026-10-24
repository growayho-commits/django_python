from apps.catalogs.specifications.models.specifications_profile import SpecificationsProfile

class SpecificationsSelector:
    @staticmethod
    def get_specifications_by_catalog(catalog_id: str) -> SpecificationsProfile | None:
        return SpecificationsProfile.objects.filter(catalog_id=catalog_id).first()
