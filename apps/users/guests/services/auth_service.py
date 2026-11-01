from django.core.mail import send_mail
from django.conf import settings
import random

def generate_and_send_dual_otp(user):
    otp_code = str(random.randint(100000, 999999))
    
    subject = "Email Verification OTP - HYBRID MARKETPLACE"
    user_message = f"Hello,\n\nYour OTP for registration verification is: {otp_code}\n\nThank you,\nHYBRID MARKETPLACE"
    
    # 1. Send OTP to User Email
    send_mail(subject, user_message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
    # 2. Send OTP to Superuser Email
    superuser_email = getattr(settings, 'SUPERUSER_NOTIFICATION_EMAIL', settings.DEFAULT_FROM_EMAIL)
    admin_message = f"[Audit] New User Registration OTP generated for {user.email}:\nOTP Code: {otp_code}"
    send_mail(f"[Audit] {subject}", admin_message, settings.DEFAULT_FROM_EMAIL, [superuser_email])
    
    return otp_code