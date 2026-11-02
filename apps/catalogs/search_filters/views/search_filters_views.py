from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.search_filters.serializers.search_filters_serializer import SearchFiltersProfileSerializer
from apps.catalogs.search_filters.dtos.search_filters_dtos import SearchFiltersCreateDTO
from apps.catalogs.search_filters.services.search_filters_service import SearchFiltersApplicationService
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class SearchFiltersSaveAPIView(APIView):
    """தேடுதல் மற்றும் வடிப்பான்களைச் சேமிப்பதற்கான API"""
    def post(self, request):
        serializer = SearchFiltersProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = SearchFiltersCreateDTO(**serializer.validated_data)
            filter_obj = SearchFiltersApplicationService.save_search_filters(dto)
            return Response(SearchFiltersProfileSerializer(filter_obj).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MachinerySearchAPIView(APIView):
    """மெஷினரி மற்றும் உதிரிப் பாகங்களைத் தேடுதல் மற்றும் விலை அடிப்படையில் வடிகட்டுவதற்கான API"""
    def get(self, request):
        query = request.GET.get('q', '')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # CoreCatalog மாடலைப் பயன்படுத்தி இயந்திரங்களைத் தேடுதல்
        items = CoreCatalog.objects.filter(is_active=True)

        if query:
            items = items.filter(
                Q(name__icontains=query) | 
                Q(sku__icontains=query) | 
                Q(brand__icontains=query) |
                Q(description__icontains=query)
            )

        if min_price:
            items = items.filter(price__gte=min_price)
        if max_price:
            items = items.filter(price__lte=max_price)

        # எளிய முறையில் தரவுகளை JSON வடிவமாக மாற்றுதல்
        data = [
            {
                "id": item.id,
                "name": item.name,
                "sku": item.sku,
                "brand": item.brand,
                "price": str(item.price),
                "stock_quantity": item.stock_quantity,
                "description": item.description,
            }
            for item in items
        ]

        return Response({
            "status": "success",
            "count": len(data),
            "results": data
        }, status=status.HTTP_200_OK)