from rest_framework import viewsets
from ..models.bank_account_profile import BankAccountProfile
from ..serializers.bank_account_serializer import BankAccountSerializer

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccountProfile.objects.all()
    serializer_class = BankAccountSerializer
    