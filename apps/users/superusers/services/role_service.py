from ..models import RoleUpgradeRequest

class SuperuserRoleService:
    @staticmethod
    def process_role_request(request_id, action):
        try:
            req = RoleUpgradeRequest.objects.get(id=request_id)
            if action == 'approve':
                req.status = 'approved'
            elif action == 'reject':
                req.status = 'rejected'
            req.save()
            return True
        except RoleUpgradeRequest.DoesNotExist:
            return False