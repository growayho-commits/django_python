from rest_framework import viewsets
from apps.common.address import Address
from apps.common.serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing address instances.
    """
    queryset = Address.objects.filter(is_active=True)
    serializer_class = AddressSerializer