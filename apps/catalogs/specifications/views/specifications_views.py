from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.specifications.serializers.specifications_serializer import SpecificationsProfileSerializer
from apps.catalogs.specifications.dtos.specifications_dtos import SpecificationsCreateDTO
from apps.catalogs.specifications.services.specifications_service import SpecificationsApplicationService

class SpecificationsSaveAPIView(APIView):
    def post(self, request):
        serializer = SpecificationsProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = SpecificationsCreateDTO(**serializer.validated_data)
            spec_obj = SpecificationsApplicationService.save_specifications(dto)
            return Response(SpecificationsProfileSerializer(spec_obj).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
