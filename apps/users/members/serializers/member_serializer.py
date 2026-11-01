from rest_framework import serializers
from apps.users.members.models import MemberProfile

class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = ['id', 'user', 'membership_tier', 'loyalty_points', 'referred_by', 'is_active_member', 'created_at', 'updated_at']
        read_only_fields = ['id', 'loyalty_points', 'created_at', 'updated_at']