from apps.users.members.models import MemberProfile

class MemberService:
    @staticmethod
    def create_member_profile(user, validated_data):
        profile, created = MemberProfile.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        return profile

    @staticmethod
    def add_loyalty_points(member_id, points):
        try:
            member = MemberProfile.objects.get(id=member_id)
            member.loyalty_points += points
            member.save()
            return member
        except MemberProfile.DoesNotExist:
            raise ValueError("Member profile does not exist.")