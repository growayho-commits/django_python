from rest_framework import serializers
from ..models import RoleRequirement, RoleUpgradeRequest

class RoleRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleRequirement
        fields = '__all__'

class RoleUpgradeRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = RoleUpgradeRequest
        fields = ['id', 'user', 'user_email', 'requested_role', 'status', 'created_at']