from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from apps.users.superusers.models.role_request import RoleUpgradeRequest
from apps.users.superusers.models.role_requirement import RoleRequirement

User = get_user_model()

@user_passes_test(lambda u: u.is_superuser)
def superuser_dashboard(request):
    """
    Superuser Dashboard View - நிர்வாகப் பக்கத்தின் முகப்பு மற்றும் கோரிக்கைகளைக் காட்டுகிறது.
    """
    role_requests = RoleUpgradeRequest.objects.all() if hasattr(RoleUpgradeRequest, 'objects') else []
    requirements = RoleRequirement.objects.all() if hasattr(RoleRequirement, 'objects') else []
    
    context = {
        'role_requests': role_requests,
        'requirements': requirements,
    }
    return render(request, 'superusers/dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser)
def network_tree_view(request):
    """
    Superuser-க்கான Hierarchical MLM Network Tree View.
    வேர்களை (Root users) கண்டறிந்து அவர்களின் கீழ் உள்ள பயனர்களை இணைக்கிறது.
    """
    if hasattr(User, 'parent'):
        root_users = User.objects.filter(parent__isnull=True, is_active=True)
    else:
        root_users = User.objects.filter(is_active=True)[:10]

    context = {
        'root_users': root_users,
    }
    return render(request, 'superusers/network_tree.html', context)


@user_passes_test(lambda u: u.is_superuser)
def handle_role_request(request, request_id, action):
    """
    பயனர்களின் ரோல் மேம்படுத்தல் கோரிக்கைகளை (Role upgrade requests) கையாளுதல்.
    """
    role_request = get_object_or_404(RoleUpgradeRequest, id=request_id)
    if action == 'approve':
        role_request.status = 'APPROVED'
        role_request.save()
    elif action == 'reject':
        role_request.status = 'REJECTED'
        role_request.save()
    
    return redirect('superusers:dashboard')


@user_passes_test(lambda u: u.is_superuser)
def update_role_requirement(request, pk):
    """
    ரோல் தேவைகளை (Role requirements) புதுப்பித்தல்.
    """
    requirement = get_object_or_404(RoleRequirement, pk=pk)
    
    if request.method == 'POST':
        # தேவைக்கேற்ப ஃபார்ம் டேட்டாவைச் சேமிக்கலாம்
        requirement.save()
        return redirect('superusers:dashboard')

    context = {
        'requirement': requirement,
    }
    return render(request, 'superusers/update_requirement.html', context)