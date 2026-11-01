from rest_framework import viewsets, permissions
from ..models.payout_profile import PayoutProfile
from ..serializers.payout_serializer import PayoutSerializer

class PayoutViewSet(viewsets.ModelViewSet):
    queryset = PayoutProfile.objects.all()
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]