from rest_framework import serializers
from apps.professional_network.models import ProfessionalProfile, ServiceRequest

class ProfessionalProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = ProfessionalProfile
        fields = [
            'id', 'user', 'user_username', 'user_email', 'title', 
            'bio', 'skills', 'hourly_rate', 'is_available', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ServiceRequestSerializer(serializers.ModelSerializer):
    client_username = serializers.ReadOnlyField(source='client.username')
    professional_title = serializers.ReadOnlyField(source='professional.title')

    class Meta:
        model = ServiceRequest
        fields = [
            'id', 'client', 'client_username', 'professional', 
            'professional_title', 'description', 'status', 
            'budget', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'client', 'created_at', 'updated_at']