from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidOTPException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Provide செய்யப்பட்ட OTP தவறானது அல்லது காலாவதியானது."
    default_code = "invalid_otp"


class AccountLockedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "தவறான லாகின் முயற்சிகள் அதிகம் என்பதால் உங்கள் கணக்கு தற்காலிகமாக பூட்டப்பட்டுள்ளது."
    default_code = "account_locked"


class TwoFactorRequiredException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "இந்தச் செயலுக்கு இருபடி பாதுகாப்பு (2FA) சரிபார்ப்பு அவசியம்."
    default_code = "two_factor_required"


class UnauthorizedAccessException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "இந்தச் சேவையை அணுக உங்களுக்கு அனுமதி இல்லை."
    default_code = "unauthorized_access"