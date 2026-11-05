from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def generate_and_send_dual_otp(user):
    otp_code = '999999'  # அல்லது உங்கள் ரேண்டம் OTP ஜெனரேட்டர் லாஜிக்
    subject = "Email Verification OTP - HYBRID MARKETPLACE"
    user_message = f"Hello,\n\nYour OTP for registration verification is: {otp_code}\n\nThank you,\nHYBRID MARKETPLACE"
    
    try:
        # மின்னஞ்சல் அனுப்ப முயற்சிக்கும்
        send_mail(subject, user_message, settings.DEFAULT_FROM_EMAIL, [user.email])
    except Exception as e:
        # SMTP அல்லது இணைப்புப் பிழை ஏற்பட்டால், லாக் செய்துவிட்டு புரோகிராம் தடையின்றி தொடர அனுமதிக்கிறோம்
        logger.warning(f"SMTP Connection failed. OTP email not sent: {e}")
        # விருப்பப்பட்டால் டெவலப்மென்ட்க்காக கன்சோலில் OTP-யை প্রিন்ட் செய்து கொள்ளலாம்:
        print(f"--- [DEBUG] OTP for {user.email}: {otp_code} ---")
    
    return otp_code