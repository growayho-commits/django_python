from rest_framework import serializers
from apps.users.core_users.models import CustomUser, UserProfile
from apps.users.core_users.services.auth_service import AuthService


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('bio', 'phone_number', 'avatar', 'is_verified')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'role', 'profile')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        # AuthService-ஐப் பயன்படுத்தி பாதுகாப்பாக பயனரை உருவாக்குதல்
        user = AuthService.register_user(**validated_data)
        
        # ப்ரொபைல் தரவுகள் இருந்தால் அவற்றை அப்டேட் செய்தல்
        if profile_data:
            AuthService.update_user_profile(user, **profile_data)
            
        return user