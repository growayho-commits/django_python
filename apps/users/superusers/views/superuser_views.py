from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from apps.users.superusers.forms.core_users_forms import GuestLoginForm, GuestRegisterForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

def guest_home_view(request):
    """
    Renders the public/guest landing page.
    """
    return render(request, 'superusers/guest_home.html')

def register_view(request):
    """
    Handles user registration and redirects to role router.
    """
    if request.method == 'POST':
        form = GuestRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('superusers:role-redirect')
    else:
        form = GuestRegisterForm()
    return render(request, 'superusers/register.html', {'form': form})

def login_view(request):
    """
    Handles secure authentication and redirects to role router.
    """
    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('superusers:role-redirect')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = GuestLoginForm()
    return render(request, 'superusers/login.html', {'form': form})

def logout_view(request):
    """
    Handles user session termination and redirects to guest home.
    """
    logout(request)
    return redirect('superusers:guest_home')

@login_required
def role_dashboard_redirect(request):
    """
    Robust role-based dashboard redirection handling Superusers, 
    Executives, Merchants, Sellers, and Members.
    """
    user = request.user
    
    # 1. Highest Priority: Superuser Status Check
    if user.is_superuser or getattr(user, 'role', '') == 'superuser' or hasattr(user, 'superuserprofile'):
        return redirect('superusers:dashboard')
    
    # 2. Check by explicit role attribute or associated profiles/groups
    role = getattr(user, 'role', '').lower()
    
    if role == 'executive' or hasattr(user, 'executiveprofile'):
        return redirect('executives:dashboard')
    elif role == 'merchant' or hasattr(user, 'merchantprofile'):
        return redirect('merchant:dashboard')
    elif role == 'seller' or hasattr(user, 'sellerprofile'):
        return redirect('sellers:dashboard')
    elif role == 'member' or hasattr(user, 'memberprofile'):
        return redirect('members:dashboard')
    
    # 3. Fallback to Superuser dashboard if user has admin/staff privileges, else member dashboard
    if user.is_staff:
        return redirect('superusers:dashboard')
        
    return redirect('members:dashboard')

@login_required
def superuser_dashboard_view(request):
    """
    Renders the superuser dashboard.
    """
    return render(request, 'superusers/dashboard.html')

class SuperuserProfileCreateOrUpdateView(LoginRequiredMixin, TemplateView):
    """
    Handles superuser profile creation and updates.
    """
    template_name = 'superusers/dashboard.html'