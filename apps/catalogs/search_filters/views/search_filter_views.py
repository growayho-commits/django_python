from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.search_filters.models.search_filter_profile import SearchFilterProfile
from apps.catalogs.search_filters.serializers.search_filter_serializer import SearchFilterSerializer
from apps.catalogs.search_filters.services.search_filter_service import SearchFilterApplicationService

class SearchFilterListCreateAPIView(APIView):
    def get(self, request):
        filters = SearchFilterApplicationService.get_all_filters()
        serializer = SearchFilterSerializer(filters, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SearchFilterSerializer(data=request.data)
        if serializer.is_valid():
            filter_obj = SearchFilterApplicationService.create_filter(serializer.validated_data)
            return Response(SearchFilterSerializer(filter_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)