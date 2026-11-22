from rest_framework import serializers
from apps.finances.bank_accounts.models.bank_account_profile import BankAccountProfile

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountProfile
        fields = '__all__'