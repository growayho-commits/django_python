from rest_framework.permissions import BasePermission


class IsEmailVerifiedPermission(BasePermission):
    """
    பயனரின் மின்னஞ்சல் OTP மூலம் சரிபார்க்கப்பட்டதா என்பதைச் சரிபார்க்கிறது.
    """
    message = "உங்கள் மின்னஞ்சல் முகவரி இன்னும் சரிபார்க்கப்படவில்லை."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        credential = getattr(request.user, "credential_profile", None)
        return credential and credential.is_email_verified


class IsActiveAccountPermission(BasePermission):
    """
    கணக்கு செயலில் உள்ளதா (Active) அல்லது சஸ்பெண்ட் செய்யப்பட்டுள்ளதா எனச் சரிபார்க்கிறது.
    """
    message = "உங்கள் கணக்கு தற்காலிகமாக முடக்கப்பட்டுள்ளது."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        security = getattr(request.user, "security_profile", None)
        return security and security.account_status == "ACTIVE"