from apps.users.executives.models import ExecutiveProfile

class ExecutiveService:
    @staticmethod
    def create_executive_profile(user, validated_data):
        profile, created = ExecutiveProfile.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        return profile

    @staticmethod
    def toggle_executive_status(executive_id):
        try:
            executive = ExecutiveProfile.objects.get(id=executive_id)
            executive.is_active_agent = not executive.is_active_agent
            executive.save()
            return executive
        except ExecutiveProfile.DoesNotExist:
            raise ValueError("Executive profile does not exist.")