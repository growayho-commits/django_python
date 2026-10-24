from django.shortcuts import get_object_or_404
from apps.core_users.models.user_model import CustomUser
from apps.core_users.models.profile_model import UserProfile

class UserSelector:
    """
    Handles all read and query operations for core users and their profiles.
    """
    
    @staticmethod
    def get_user_by_id(user_id: int) -> CustomUser:
        """Fetch an active user by their primary key ID."""
        return get_object_or_404(CustomUser, id=user_id, is_active=True)

    @staticmethod
    def get_user_by_email(email: str) -> CustomUser:
        """Fetch an active user by their email address."""
        return get_object_or_404(CustomUser, email=email, is_active=True)

    @staticmethod
    def get_user_profile(user: CustomUser) -> UserProfile:
        """Fetch the profile associated with a specific user."""
        return get_object_or_404(UserProfile, user=user)

    @staticmethod
    def list_active_users():
        """Return a queryset of all active users with their profiles pre-fetched."""
        return CustomUser.objects.filter(is_active=True).select_related('profile')