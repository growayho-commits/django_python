from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from apps.users.guests.forms.core_users_forms import GuestLoginForm, GuestRegisterForm

def guest_home_view(request):
    """
    தளத்திற்கு வரும் விருந்தினர்களுக்கான முகப்புப் பக்கம் (guest_home.html)
    """
    return render(request, 'guests/guest_home.html')

def register_view(request):
    if request.method == 'POST':
        form = GuestRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('guests:role_dashboard_redirect')
    else:
        form = GuestRegisterForm()
    return render(request, 'guests/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = GuestLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('guests:role_dashboard_redirect')
    else:
        form = GuestLoginForm()
    return render(request, 'guests/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('guests:login')

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
    return redirect(role_redirects.get(user.role, 'guests:login'))