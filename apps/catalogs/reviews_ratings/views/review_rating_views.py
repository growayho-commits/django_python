from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.reviews_ratings.models.review_rating_profile import ReviewRatingProfile
from apps.catalogs.reviews_ratings.serializers.review_rating_serializer import ReviewRatingSerializer
from apps.catalogs.reviews_ratings.services.review_rating_service import ReviewRatingApplicationService

class ReviewRatingListCreateAPIView(APIView):
    def get(self, request):
        reviews = ReviewRatingApplicationService.get_all_reviews()
        serializer = ReviewRatingSerializer(reviews, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReviewRatingSerializer(data=request.data)
        if serializer.is_valid():
            review = ReviewRatingApplicationService.create_review(serializer.validated_data)
            return Response(ReviewRatingSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)