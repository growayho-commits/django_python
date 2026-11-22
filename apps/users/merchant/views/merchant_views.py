from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def overview_view(request):
    return render(request, 'merchant/overview.html', {'active_tab': 'overview'})


@login_required
def catalogs_view(request):
    return render(request, 'merchant/catalogs.html', {'active_tab': 'catalogs'})


@login_required
def bundles_view(request):
    return render(request, 'merchant/bundles.html', {'active_tab': 'bundles'})


@login_required
def orders_view(request):
    return render(request, 'merchant/orders.html', {'active_tab': 'orders'})


@login_required
def logistics_view(request):
    return render(request, 'merchant/logistics.html', {'active_tab': 'logistics'})


@login_required
def finances_view(request):
    return render(request, 'merchant/finances.html', {'active_tab': 'finances'})


@login_required
def profile_view(request):
    return render(request, 'merchant/profile.html', {'active_tab': 'profile'})