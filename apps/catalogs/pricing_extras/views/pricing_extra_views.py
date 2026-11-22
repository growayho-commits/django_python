from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.pricing_extras.models.pricing_extra_profile import PricingExtraProfile
from apps.catalogs.pricing_extras.serializers.pricing_extra_serializer import PricingExtraSerializer
from apps.catalogs.pricing_extras.services.pricing_extra_service import PricingExtraApplicationService

class PricingExtraListCreateAPIView(APIView):
    def get(self, request):
        extras = PricingExtraApplicationService.get_all_extras()
        serializer = PricingExtraSerializer(extras, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PricingExtraSerializer(data=request.data)
        if serializer.is_valid():
            extra = PricingExtraApplicationService.create_extra(serializer.validated_data)
            return Response(PricingExtraSerializer(extra).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)