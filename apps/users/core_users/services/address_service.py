import random
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from apps.core_users.models.user_model import CustomUser
from apps.core_users.models.profile_model import UserProfile

class AuthService:
    """
    Handles user registration, 6-digit OTP generation, and email dispatch 
    to both the user and the superuser.
    """

    @staticmethod
    @transaction.atomic
    def register_user(*, email: str, password: str, role: str = 'member', **extra_fields) -> CustomUser:
        # 6 இலக்க ஒடிபி உருவாக்குதல்
        otp_code = str(random.randint(100000, 999999))
        
        # 1. பயனரை டேட்டாபேஸில் உருவாக்குதல்
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            role=role,
            otp=otp_code,
            is_email_verified=False,
            **extra_fields
        )
        
        # 2. ப்ரொபைல் உருவாக்குதல்
        UserProfile.objects.create(user=user)
        
        # 3. பயனர் உள்ளீடு செய்த உண்மையான மின்னஞ்சலுக்கு OTP அனுப்புதல்
        user_subject = "Verification OTP - Hybrid Marketplace"
        user_message = f"Hello,\n\nYour email verification OTP is: {otp_code}\nPlease use this code to activate your account."
        
        send_mail(
            subject=user_subject,
            message=user_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],  # பயனரின் உண்மையான மெயில் ஐடி
            fail_silently=False,
        )
        
        # 4. சூப்பர் யூசருக்கு அறிவிப்பு மற்றும் காப்பி அனுப்புதல்
        admin_subject = f"New User Signup: {email}"
        admin_message = f"A new user has registered on the platform.\n\nUser Email: {email}\nRole: {role}\nOTP: {otp_code}"
        
        try:
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.SUPERUSER_EMAIL],  # சூப்பர் யூசரின் மெயில் ஐடி
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email to superuser: {e}")

        return user