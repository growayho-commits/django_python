from rest_framework import serializers
from apps.users.core_users.models import (
    User, 
    UserCredentialProfile, 
    UserPersonalProfile, 
    UserProfessionalProfile, 
    UserSkillService,
    BusinessEnterpriseProfile
)


class UserSkillServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkillService
        fields = ["id", "skill_or_service_name", "experience_years", "description"]


class UserProfessionalProfileSerializer(serializers.ModelSerializer):
    skills_and_services = UserSkillServiceSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfessionalProfile
        fields = [
            "primary_industry", "team_size", "service_coverage_type", 
            "service_pincodes_or_areas", "working_hours_start", 
            "working_hours_end", "weekly_off_days", "skills_and_services"
        ]


class UserPersonalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalProfile
        fields = [
            "first_name", "last_name", "phone_number", "date_of_birth", 
            "gender", "avatar", "address_line1", "address_line2", 
            "city", "state", "pincode", "country"
        ]


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    assigned_merchant_email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)