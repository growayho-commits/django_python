from rest_framework import serializers
from .address import Address

class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for Address model with custom validation for pincode.
    """
    class Meta:
        model = Address
        fields = [
            'id', 
            'address_line_1', 
            'address_line_2', 
            'landmark', 
            'city', 
            'state', 
            'country', 
            'pincode', 
            'created_at', 
            'updated_at', 
            'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_pincode(self, value):
        """Custom field validation to ensure pincode contains only digits and is of proper length"""
        if not value.isdigit():
            raise serializers.ValidationError("Pincode must contain only digits.")
        if len(value) != 6:  # Assuming Indian postal codes (PIN) of 6 digits
            raise serializers.ValidationError("Pincode must be exactly 6 digits long.")
        return value