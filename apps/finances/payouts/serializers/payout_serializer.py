from rest_framework import serializers
from ..models.payout_profile import PayoutProfile

class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutProfile
        fields = ['id', 'vendor', 'amount', 'status', 'transaction_reference', 'created_at', 'processed_at']
        read_only_fields = ['id', 'created_at', 'processed_at']