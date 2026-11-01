from django.conf import settings
from django.db import models

class MemberProfile(models.Model):
    MEMBER_TIERS = (
        ('standard', 'Standard Member'),
        ('premium', 'Premium Member'),
        ('vip', 'VIP Member'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member_profile')
    membership_tier = models.CharField(max_length=50, choices=MEMBER_TIERS, default='standard')
    loyalty_points = models.PositiveIntegerField(default=0)
    referred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='referrals')
    is_active_member = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_membership_tier_display()})"