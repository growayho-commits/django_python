import uuid
from django.db import models

class ReviewsRatingsProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.ForeignKey('core_catalogs.CoreCatalog', on_delete=models.CASCADE, related_name='reviews')
    user_id = models.CharField(max_length=100, db_index=True)
    star_rating = models.PositiveSmallIntegerField(default=5)
    review_comment = models.TextField()
    user_uploaded_images = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catalog_reviews_ratings_profile'

    @classmethod
    def create_review(cls, catalog_obj, dto) -> 'ReviewsRatingsProfile':
        if not (1 <= dto.star_rating <= 5):
            raise ValueError("Domain Rule Error: Star rating must be between 1 and 5.")
        return cls.objects.create(
            catalog=catalog_obj,
            user_id=dto.user_id,
            star_rating=dto.star_rating,
            review_comment=dto.review_comment,
            user_uploaded_images=dto.user_uploaded_images
        )
