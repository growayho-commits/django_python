from rest_framework import serializers
from apps.users.superusers.models import RoleUpgradeRequest

class RoleUpgradeRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = RoleUpgradeRequest
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']