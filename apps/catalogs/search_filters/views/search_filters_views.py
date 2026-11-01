from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.search_filters.serializers.search_filters_serializer import SearchFiltersProfileSerializer
from apps.catalogs.search_filters.dtos.search_filters_dtos import SearchFiltersCreateDTO
from apps.catalogs.search_filters.services.search_filters_service import SearchFiltersApplicationService

class SearchFiltersSaveAPIView(APIView):
    def post(self, request):
        serializer = SearchFiltersProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = SearchFiltersCreateDTO(**serializer.validated_data)
            filter_obj = SearchFiltersApplicationService.save_search_filters(dto)
            return Response(SearchFiltersProfileSerializer(filter_obj).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
