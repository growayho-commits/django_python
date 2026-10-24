from django.db import transaction
from apps.catalogs.reviews_ratings.dtos.reviews_ratings_dtos import ReviewCreateDTO
from apps.catalogs.reviews_ratings.models.reviews_ratings_profile import ReviewsRatingsProfile
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class ReviewsRatingsApplicationService:
    @staticmethod
    @transaction.atomic
    def post_review(dto: ReviewCreateDTO) -> ReviewsRatingsProfile:
        catalog = CoreCatalog.objects.get(id=dto.catalog_id)
        return ReviewsRatingsProfile.create_review(catalog_obj=catalog, dto=dto)
