from rest_framework import serializers
from apps.users.superusers.models import SuperuserProfile

class SuperuserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperuserProfile
        fields = ['id', 'user', 'security_level', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']