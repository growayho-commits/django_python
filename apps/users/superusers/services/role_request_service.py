from django.db import transaction
from apps.users.superusers.models import RoleUpgradeRequest
from apps.users.members.models import MemberProfile
from apps.users.sellers.models import SellerProfile
from apps.users.merchants.models import MerchantProfile
from apps.users.executives.models import ExecutiveProfile


def get_user_current_role(user):
    if getattr(user, 'is_superuser', False):
        return 'superuser'

    latest_approved = (
        RoleUpgradeRequest.objects.filter(user=user, status='approved')
        .order_by('-updated_at', '-id')
        .first()
    )
    if latest_approved:
        return latest_approved.requested_role

    if ExecutiveProfile.objects.filter(user=user, is_active_agent=True).exists():
        return 'executive'
    if MerchantProfile.objects.filter(user=user).exists():
        return 'merchant'
    if SellerProfile.objects.filter(user=user).exists():
        return 'seller'
    if MemberProfile.objects.filter(user=user, is_active_member=True).exists():
        return 'member'
    return 'member'


class RoleUpgradeRequestService:
    """
    Handles role upgrade requests and soft role switching without deleting historical profiles.
    """

    @staticmethod
    @transaction.atomic
    def update_status_and_notify(request_id, action, remarks=''):
        try:
            role_req = RoleUpgradeRequest.objects.select_related('user').get(pk=request_id)
            target_user = role_req.user

            if action == 'approve':
                role_req.status = 'approved'
                new_role = role_req.requested_role

                # Soft-deactivate previous active flags while preserving history
                MemberProfile.objects.filter(user=target_user).update(is_active_member=(new_role == 'member'))
                ExecutiveProfile.objects.filter(user=target_user).update(is_active_agent=(new_role == 'executive'))

                if new_role == 'seller':
                    SellerProfile.objects.get_or_create(user=target_user)
                elif new_role == 'merchant':
                    MerchantProfile.objects.get_or_create(user=target_user)
                elif new_role == 'executive':
                    ExecutiveProfile.objects.get_or_create(user=target_user)
                elif new_role == 'member':
                    MemberProfile.objects.get_or_create(user=target_user)

            elif action == 'reject':
                role_req.status = 'rejected'
            elif action in ['reconsider', 'reconsidered']:
                role_req.status = 'reconsidered'
            else:
                raise ValueError('Invalid action specified.')

            if remarks:
                role_req.admin_remarks = remarks
            role_req.save()

            return role_req
        except RoleUpgradeRequest.DoesNotExist:
            raise Exception('Role upgrade request not found.')