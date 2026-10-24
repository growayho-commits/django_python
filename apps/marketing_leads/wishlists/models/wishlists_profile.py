import uuid
from django.db import models

class WishlistProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=100, db_index=True)
    catalog = models.ForeignKey('core_catalogs.CoreCatalog', on_delete=models.CASCADE, related_name='in_wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catalog_wishlist_profile'
        unique_together = ('user_id', 'catalog')
