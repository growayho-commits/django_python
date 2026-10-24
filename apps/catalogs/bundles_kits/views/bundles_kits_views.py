from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.bundles_kits.serializers.bundles_kits_serializer import BundlesKitsProfileSerializer
from apps.catalogs.bundles_kits.dtos.bundles_kits_dtos import BundleKitCreateDTO
from apps.catalogs.bundles_kits.services.bundles_kits_service import BundlesKitsApplicationService

class BundleKitAddAPIView(APIView):
    def post(self, request):
        serializer = BundlesKitsProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = BundleKitCreateDTO(**serializer.validated_data)
            try:
                bundle_obj = BundlesKitsApplicationService.add_item_to_bundle(dto)
                return Response(BundlesKitsProfileSerializer(bundle_obj).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
