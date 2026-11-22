from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.attributes.models.attribute_profile import AttributeProfile
from apps.catalogs.attributes.serializers.attribute_serializer import AttributeSerializer
from apps.catalogs.attributes.services.attribute_service import AttributeApplicationService

class AttributeListCreateAPIView(APIView):
    def get(self, request):
        attributes = AttributeApplicationService.get_all_attributes()
        serializer = AttributeSerializer(attributes, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            attribute = AttributeApplicationService.create_attribute(serializer.validated_data)
            return Response(AttributeSerializer(attribute).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)