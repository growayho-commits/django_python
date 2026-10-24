from django.utils import timezone
from datetime import timedelta
from apps.users.core_users.exceptions.security_exceptions import InvalidOTPException


def validate_otp_expiration(credential_profile):
    """
    OTP உருவாக்கப்பட்டதிலிருந்து 5 நிமிடங்கள் மட்டுமே செல்லுபடியாகும் என்பதைச் சரிபார்க்கிறது.
    """
    if not credential_profile.otp_created_at:
        raise InvalidOTPException("OTP உருவாக்கப்படவில்லை.")
    
    expiration_time = credential_profile.otp_created_at + timedelta(minutes=5)
    if timezone.now() > expiration_time:
        raise InvalidOTPException("OTP காலாவதியாகிவிட்டது. புதிய OTP-ஐப் பெறவும்.")