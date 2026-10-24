from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.reviews_ratings.serializers.reviews_ratings_serializer import ReviewsRatingsProfileSerializer
from apps.catalogs.reviews_ratings.dtos.reviews_ratings_dtos import ReviewCreateDTO
from apps.catalogs.reviews_ratings.services.reviews_ratings_service import ReviewsRatingsApplicationService

class ReviewCreateAPIView(APIView):
    def post(self, request):
        serializer = ReviewsRatingsProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = ReviewCreateDTO(**serializer.validated_data)
            try:
                review_obj = ReviewsRatingsApplicationService.post_review(dto)
                return Response(ReviewsRatingsProfileSerializer(review_obj).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
