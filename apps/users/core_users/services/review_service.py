from django.db import transaction
from apps.users.core_users.models import UserReview, UserProfessionalProfile


@transaction.atomic
def create_professional_review(reviewer, professional_profile_id, rating, comment=""):
    """
    சேவை வெற்றிகரமாக முடிந்ததும் வாடிக்கையாளர் ஸ்டார் ரேட்டிங் வழங்குவதை உறுதிசெய்து சேமிக்கிறது.
    """
    if not (1 <= rating <= 5):
        raise ValueError("ஸ்டார் ரேட்டிங் 1 முதல் 5க்குள் இருக்க வேண்டும்.")

    professional = UserProfessionalProfile.objects.get(id=professional_profile_id)

    review = UserReview.objects.create(
        professional=professional,
        reviewer=reviewer,
        rating=rating,
        comment=comment,
        is_completed=True
    )
    return review