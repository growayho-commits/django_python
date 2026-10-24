from django.db.models import Avg
from apps.users.core_users.models import UserProfessionalProfile


def search_professionals_with_ratings(skill_name=None, pincode=None):
    """
    குறிப்பிட்ட திறன் (எ.கா: Electrician) மற்றும் பின்கோட்டின் அடிப்படையில் 
    தொழில் வல்லுநர்களைத் தேடி, அவர்களின் சராசரி ஸ்டார் ரேட்டிங்குடன் பட்டியலிடுதல்.
    """
    queryset = UserProfessionalProfile.objects.select_related(
        "user", "user__personal_profile"
    ).prefetch_related("skills_and_services", "reviews")

    # திறன் மூலம் வடிகட்டுதல்
    if skill_name:
        queryset = queryset.filter(skills_and_services__skill_or_service_name__icontains=skill_name)
    
    # பின்கோடு மூலம் வடிகட்டுதல்
    if pincode:
        queryset = queryset.filter(service_pincodes_or_areas__contains=pincode)

    # வாடிக்கையாளர்கள் வழங்கிய சராசரி ரேட்டிங்கை (Average Rating) கணக்கிடுதல்
    return queryset.annotate(average_rating=Avg("reviews__rating"))