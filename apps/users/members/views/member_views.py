from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalogs.catalog_wishlist.models.catalog_wishlist_profile import CatalogWishlistProfile
from apps.catalogs.categories.models.category_profile import CategoryProfile
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.marketing_leads.carts.models.cart_profile import CartItem, CartProfile
from apps.users.superusers.forms.role_forms import RoleUpgradeRequestForm
from apps.users.superusers.models import RoleUpgradeRequest


def _get_catalog_context(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()

    products = (
        CoreCatalogProfile.objects.filter(is_active=True)
        .select_related('category', 'owner')
        .prefetch_related('inventories')
        .order_by('-created_at')
    )
    if category_id:
        products = products.filter(category_id=category_id)
    if search_query:
        products = products.filter(name__icontains=search_query)

    categories = CategoryProfile.objects.filter(is_active=True).order_by('name')
    wishlist_skus = set(
        CatalogWishlistProfile.objects.filter(user_identifier=request.user.email)
        .values_list('product_sku', flat=True)
    )
    return {
        'catalog_products': products,
        'categories': categories,
        'selected_category': category_id or '',
        'search_query': search_query,
        'wishlist_skus': wishlist_skus,
    }


@login_required
def member_dashboard_view(request):
    user = request.user
    my_requests = RoleUpgradeRequest.objects.filter(user=user).order_by('-created_at')

    pending_role_names = list(
        my_requests.filter(status='pending').values_list('requested_role', flat=True)
    )
    excluded_roles = set(pending_role_names + ['member'])

    if request.method == 'POST':
        form = RoleUpgradeRequestForm(request.POST)
        if form.is_valid():
            role_req = form.save(commit=False)
            if role_req.requested_role in excluded_roles:
                messages.error(request, 'You already have a pending request for this role.')
            else:
                role_req.user = user
                role_req.status = 'pending'
                role_req.save()
                messages.success(request, 'Your upgrade request has been submitted successfully!')
                return redirect('/api/v1/users/members/dashboard/#requests')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoleUpgradeRequestForm()

    if 'requested_role' in form.fields:
        current_choices = form.fields['requested_role'].choices
        form.fields['requested_role'].choices = [
            (val, label) for val, label in current_choices
            if val.lower() not in [r.lower() for r in excluded_roles]
        ]

    context = {
        'form': form,
        'my_requests': my_requests,
        **_get_catalog_context(request),
    }
    return render(request, 'members/dashboard.html', context)


@login_required
def member_catalogs_view(request):
    """Shared Marketplace Catalog view accessible by all authenticated user roles."""
    return render(request, 'members/catalogs_page.html', _get_catalog_context(request))


@login_required
def add_to_cart_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(CoreCatalogProfile, pk=product_id, is_active=True)
        qty = max(1, int(request.POST.get('quantity', 1)))
        cart, _ = CartProfile.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=str(product.id),
            defaults={'quantity': qty, 'unit_price': product.base_price},
        )
        if not created:
            item.quantity += qty
            item.unit_price = product.base_price
            item.save()

        messages.success(request, f'Added "{product.name}" (Qty: {qty}) to your cart.')
    return redirect(request.META.get('HTTP_REFERER', 'users:members:catalogs'))


@login_required
def toggle_wishlist_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(CoreCatalogProfile, pk=product_id, is_active=True)
        product_key = f"PROD-{product.id}"
        existing = CatalogWishlistProfile.objects.filter(
            user_identifier=request.user.email,
            product_sku=product_key,
        ).first()

        if existing:
            existing.delete()
            messages.info(request, f'Removed "{product.name}" from your wishlist.')
        else:
            CatalogWishlistProfile.objects.create(
                user_identifier=request.user.email,
                product_sku=product_key,
                notes=product.name,
            )
            messages.success(request, f'Saved "{product.name}" to your wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'users:members:catalogs'))


@login_required
def member_orders_view(request):
    return render(request, 'members/orders.html')


@login_required
def member_profile_view(request):
    return render(request, 'members/profile.html')


@login_required
def member_requests_view(request):
    return redirect('/api/v1/users/members/dashboard/#requests')


@login_required
def member_services_view(request):
    return render(request, 'members/services.html')