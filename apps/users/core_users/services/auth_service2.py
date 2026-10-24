from django.utils import timezone
from django.db import transaction
from apps.users.core_users.models import (
    User,
    UserCredentialProfile,
    UserPersonalProfile,
    UserProfessionalProfile,
    BusinessEnterpriseProfile,
    UserSecurityProfile
)


@transaction.atomic
def register_user_with_5_tier_profiles(email, password, assigned_merchant_email=None):
    """
    பயனர் பதிவு செய்யும் போதே 5 வகையான ப்ரொஃபைல் அட்டவணைகளையும் இணைத்து உருவாக்கும் Core Service.
    """
    # 1. முதன்மை யூசர் (User Model)
    user = User.objects.create_user(email=email, password=password)

    # 2. பேசிக் ப்ரொபைல் (Credential & Assignment)
    UserCredentialProfile.objects.create(
        user=user,
        assigned_merchant_email=assigned_merchant_email,
        is_email_verified=False,
        terms_accepted=True
    )

    # 3. பர்சனல் ப்ரொபைல் (Personal Profile)
    UserPersonalProfile.objects.create(user=user)

    # 4. ப்ரொபஷனல் ப்ரொபைல் (Professional Profile)
    UserProfessionalProfile.objects.create(user=user)

    # 5. பிசினஸ் ப்ரொபைல் (Business Profile)
    BusinessEnterpriseProfile.objects.create(user=user, company_name="GROWAY SOLUTIONS")

    # 6. செக்யூரிட்டி ப்ரொபைல் (Security & Compliance Profile)
    UserSecurityProfile.objects.create(user=user, data_privacy_consent=True)

    return user