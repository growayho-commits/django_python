from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from apps.users.guests.forms.core_users_forms import GuestRegistrationForm, GuestLoginForm
from apps.users.guests.services.auth_service import generate_and_send_dual_otp
from apps.users.guests.models import CoreUser

def register_view(request):
    if request.method == 'POST':
        form = GuestRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'member'  # Converted to Member upon registration
            user.is_verified = False
            user.save()
            
            otp = generate_and_send_dual_otp(user)
            request.session['verify_user_id'] = user.id
            request.session['generated_otp'] = otp
            return redirect('verify_otp')
    else:
        form = GuestRegistrationForm()
    return render(request, 'guests/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('role_dashboard_redirect')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = GuestLoginForm()
    return render(request, 'guests/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def role_dashboard_redirect(request):
    user = request.user
    role_redirects = {
        'superuser': 'superusers:dashboard',
        'seller': 'sellers:dashboard',
        'executive': 'executives:dashboard',
        'merchant': 'merchant:dashboard',
        'member': 'members:dashboard',
    }
    return redirect(role_redirects.get(user.role, 'guest_home'))