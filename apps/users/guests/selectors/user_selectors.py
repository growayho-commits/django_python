from django.contrib.auth import get_user_model

User = get_user_model()

class UserSelector:
    @staticmethod
    def get_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
