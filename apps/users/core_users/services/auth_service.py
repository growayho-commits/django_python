from django.db import transaction
from apps.users.core_users.models import CustomUser, UserProfile

class AuthService:
    """
    Handles user authentication, creation, and profile mutation business logic.
    """

    @staticmethod
    @transaction.atomic
    def register_user(*, email: str, password: str, role: str = 'member', **extra_fields) -> CustomUser:
        """
        Registers a new CustomUser with email-only authentication and automatically initializes their UserProfile.
        """
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            role=role,
            **extra_fields
        )
        
        # Automatically create an associated UserProfile
        UserProfile.objects.create(user=user)
        
        return user

    @staticmethod
    @transaction.atomic
    def update_user_profile(user: CustomUser, **profile_data) -> UserProfile:
        """
        Updates the profile information for a given user.
        """
        profile = user.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        return profile