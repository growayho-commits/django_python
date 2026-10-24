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
def register_user_with_profiles(email, password, assigned_merchant_email=None):
    """
    புதிய பயனரைப் பதிவு செய்யும் போது, அதற்கான அனைத்து 5 ப்ரொஃபைல் அட்டவணைகளையும் தானாக உருவாக்கும்.
    """
    # 1. முதன்மை யூசர் உருவாக்கம்
    user = User.objects.create_user(email=email, password=password)

    # 2. பேசிக் / கிரெடென்ஷியல் ப்ரொஃபைல்
    UserCredentialProfile.objects.create(
        user=user,
        assigned_merchant_email=assigned_merchant_email,
        otp_code="123456",  # டெஸ்டிங்கிற்கான மாதிரி OTP (உண்மையில் ரேண்டமாக உருவாக்கப்படும்)
        otp_created_at=timezone.now()
    )

    # 3. பர்சனல் ப்ரொஃபைல் (வெற்றுப் பதிவுகள்)
    UserPersonalProfile.objects.create(user=user)

    # 4. ப்ரொபஷனல் ப்ரொஃபைல்
    UserProfessionalProfile.objects.create(user=user)

    # 5. பிசினஸ் ப்ரொஃபைல்
    BusinessEnterpriseProfile.objects.create(user=user, company_name="Default Company")

    # 6. செக்யூரிட்டி ப்ரொஃபைல்
    UserSecurityProfile.objects.create(user=user)

    return user