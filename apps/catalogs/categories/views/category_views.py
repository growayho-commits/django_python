from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.categories.models.category_profile import CategoryProfile
from apps.catalogs.categories.serializers.category_serializer import CategorySerializer
from apps.catalogs.categories.services.category_service import CategoryApplicationService

class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = CategoryApplicationService.get_all_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = CategoryApplicationService.create_category(serializer.validated_data)
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)