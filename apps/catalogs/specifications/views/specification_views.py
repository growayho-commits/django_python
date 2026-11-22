from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.specifications.models.specification_profile import SpecificationProfile
from apps.catalogs.specifications.serializers.specification_serializer import SpecificationSerializer
from apps.catalogs.specifications.services.specification_service import SpecificationApplicationService

class SpecificationListCreateAPIView(APIView):
    def get(self, request):
        specifications = SpecificationApplicationService.get_all_specifications()
        serializer = SpecificationSerializer(specifications, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SpecificationSerializer(data=request.data)
        if serializer.is_valid():
            specification = SpecificationApplicationService.create_specification(serializer.validated_data)
            return Response(SpecificationSerializer(specification).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)