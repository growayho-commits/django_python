from rest_framework import viewsets, permissions
from ..models.tax_profile import TaxProfile
from ..serializers.tax_serializer import TaxSerializer

class TaxViewSet(viewsets.ModelViewSet):
    queryset = TaxProfile.objects.all()
    serializer_class = TaxSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]