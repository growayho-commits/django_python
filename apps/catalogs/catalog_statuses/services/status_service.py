# apps/catalogs/catalog_statuses/services/status_service.py

from apps.catalogs.catalog_statuses.models.status_profile import CatalogStatusProfile

class CatalogStatusService:
    @staticmethod
    def update_status(catalog, new_status, remarks=None):
        """தயாரிப்புக்கான நிலையைப் புதுப்பிக்க அல்லது புதிய நிலையை உருவாக்க (Update/Create Status)"""
        status_obj, created = CatalogStatusProfile.objects.get_or_create(
            catalog=catalog,
            defaults={'status': new_status, 'remarks': remarks}
        )
        if not created:
            status_obj.status = new_status
            if remarks:
                status_obj.remarks = remarks
            status_obj.save()
            
        return status_obj