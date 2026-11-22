from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.bundles_kits.models.bundle_kit_profile import BundleKitProfile
from apps.catalogs.bundles_kits.serializers.bundle_kit_serializer import BundleKitSerializer
from apps.catalogs.bundles_kits.services.bundle_kit_service import BundleKitApplicationService

class BundleKitListCreateAPIView(APIView):
    def get(self, request):
        bundles = BundleKitApplicationService.get_all_bundles()
        serializer = BundleKitSerializer(bundles, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BundleKitSerializer(data=request.data)
        if serializer.is_valid():
            bundle = BundleKitApplicationService.create_bundle(serializer.validated_data)
            return Response(BundleKitSerializer(bundle).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)