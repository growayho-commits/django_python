from apps.users.core_users.models import UserProfessionalProfile, UserPersonalProfile


def get_professionals_by_pincode(pincode: str):
    """
    குறிப்பிட்ட பின்கோட்டில் சேவை வழங்கும் அனைத்து தொழில் வல்லுநர்களின் (Professionals) பட்டியலைக் கொண்டுவரும்.
    """
    # JSONField-ல் பின்கோடு உள்ளதா எனத் தேடுதல்
    return UserProfessionalProfile.objects.filter(
        service_pincodes_or_areas__contains=pincode
    ).select_related("user", "user__personal_profile")


def get_user_complete_profile(user):
    """
    ஒரு பயனரின் அனைத்து 5 ப்ரொஃபைல் விவரங்களையும் சேர்த்து ஒரே இடத்தில் வழங்கும்.
    """
    return {
        "user": user,
        "credential": getattr(user, "credential_profile", None),
        "personal": getattr(user, "personal_profile", None),
        "professional": getattr(user, "professional_profile", None),
        "skills": getattr(getattr(user, "professional_profile", None), "skills_and_services", None),
        "business": getattr(user, "business_profile", None),
        "security": getattr(user, "security_profile", None),
    }