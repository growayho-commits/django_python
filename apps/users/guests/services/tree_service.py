from apps.users.guests.models import BasicProfile

def get_user_tree_and_upline(user):
    """
    Role-based tree view and upline resolution
    """
    data = {
        'current_user': user,
        'upline': [],
        'downline': []
    }

    # 1. Upline resolution
    if user.role == 'member':
        if user.assigned_merchant:
            data['upline'].append(user.assigned_merchant)
            if user.assigned_merchant.assigned_executive:
                data['upline'].append(user.assigned_merchant.assigned_executive)
                if user.assigned_merchant.assigned_executive.assigned_seller:
                    data['upline'].append(user.assigned_merchant.assigned_executive.assigned_seller)
    elif user.role == 'merchant':
        if user.assigned_executive:
            data['upline'].append(user.assigned_executive)
            if user.assigned_executive.assigned_seller:
                data['upline'].append(user.assigned_executive.assigned_seller)
    elif user.role == 'executive':
        if user.assigned_seller:
            data['upline'].append(user.assigned_seller)

    # 2. Downline / Tree view resolution based on role
    if user.role == 'superuser':
        # Superuser can see all tree views across roles
        data['all_sellers'] = BasicProfile.objects.filter(role='seller')
        data['all_executives'] = BasicProfile.objects.filter(role='executive')
        data['all_merchants'] = BasicProfile.objects.filter(role='merchant')
        data['all_members'] = BasicProfile.objects.filter(role='member')

    elif user.role == 'seller':
        # Seller can see all executives by tree view
        data['executives'] = user.seller_executives.all()
        # and through executives -> merchants -> members

    elif user.role == 'executive':
        # Executive can see their merchants and members
        merchants = user.executive_merchants.all()
        data['merchants'] = merchants
        data['members'] = BasicProfile.objects.filter(assigned_merchant__in=merchants)

    elif user.role == 'merchant':
        # Merchant can see their members
        data['members'] = user.merchant_members.all()

    return data