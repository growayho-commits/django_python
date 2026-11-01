from rest_framework import serializers
from ..models.tax_profile import TaxProfile

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxProfile
        fields = ['id', 'tax_name', 'percentage', 'is_active', 'created_at']