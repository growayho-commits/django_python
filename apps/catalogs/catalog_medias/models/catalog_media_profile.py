import uuid
from django.db import models

class CatalogMediaProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.OneToOneField('core_catalogs.CoreCatalog', on_delete=models.CASCADE, related_name='media_suite')
    primary_image_url = models.URLField(max_length=500)
    gallery_image_urls = models.JSONField(default=list, blank=True)
    interactive_360_urls = models.JSONField(default=list, blank=True)
    demo_video_url = models.URLField(max_length=500, blank=True, null=True)
    model_3d_gltf_url = models.URLField(max_length=500, blank=True, null=True)
    ar_usdz_url = models.URLField(max_length=500, blank=True, null=True)
    dxf_drawing_url = models.URLField(max_length=500, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_media_profile'

    @classmethod
    def create_or_update_media(cls, catalog_obj, dto) -> 'CatalogMediaProfile':
        if not dto.primary_image_url.strip():
            raise ValueError("Domain Rule Error: Primary image URL is mandatory for media suite.")
        obj, _ = cls.objects.update_or_create(
            catalog=catalog_obj,
            defaults={
                'primary_image_url': dto.primary_image_url,
                'gallery_image_urls': dto.gallery_image_urls,
                'interactive_360_urls': dto.interactive_360_urls,
                'demo_video_url': dto.demo_video_url,
                'model_3d_gltf_url': dto.model_3d_gltf_url,
                'ar_usdz_url': dto.ar_usdz_url,
                'dxf_drawing_url': dto.dxf_drawing_url
            }
        )
        return obj
