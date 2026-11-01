import uuid
from django.db import models

class SearchFiltersProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.OneToOneField('core_catalogs.CoreCatalog', on_delete=models.CASCADE, related_name='search_filter')
    tags = models.JSONField(default=list, blank=True)
    meta_keywords = models.JSONField(default=list, blank=True)
    faceted_search_json = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'catalog_search_filters_profile'

    @classmethod
    def save_filters(cls, catalog_obj, dto) -> 'SearchFiltersProfile':
        obj, _ = cls.objects.update_or_create(
            catalog=catalog_obj,
            defaults={
                'tags': dto.tags,
                'meta_keywords': dto.meta_keywords,
                'faceted_search_json': dto.faceted_search_json
            }
        )
        return obj
