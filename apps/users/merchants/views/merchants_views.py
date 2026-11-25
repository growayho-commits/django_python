from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def overview_view(request):
    return render(request, 'merchants/overview.html', {'active_tab': 'overview'})


@login_required
def catalogs_view(request):
    return render(request, 'merchants/catalogs.html', {'active_tab': 'catalogs'})


@login_required
def bundles_view(request):
    return render(request, 'merchants/bundles.html', {'active_tab': 'bundles'})


@login_required
def orders_view(request):
    return render(request, 'merchants/orders.html', {'active_tab': 'orders'})


@login_required
def logistics_view(request):
    return render(request, 'merchants/logistics.html', {'active_tab': 'logistics'})


@login_required
def finances_view(request):
    return render(request, 'merchants/finances.html', {'active_tab': 'finances'})


@login_required
def profile_view(request):
    return render(request, 'merchants/profile.html', {'active_tab': 'profile'})