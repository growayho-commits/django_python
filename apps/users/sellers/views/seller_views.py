from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.catalogs.categories.models.category_profile import CategoryProfile
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile


@login_required
def overview_view(request):
    products_qs = CoreCatalogProfile.objects.filter(owner=request.user)
    inventories_qs = InventoryProfile.objects.filter(owner=request.user)

    total_products = products_qs.filter(is_active=True).count()
    low_stock_count = sum(1 for inv in inventories_qs if inv.is_low_stock or inv.stock_quantity <= 0)

    return render(request, 'sellers/overview.html', {
        'active_tab': 'overview',
        'total_products': total_products,
        'low_stock_count': low_stock_count,
    })


@login_required
def products_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category_id') or None
        base_price = request.POST.get('base_price') or 0
        unit = request.POST.get('unit') or 'unit'
        description = request.POST.get('description', '').strip()

        if name:
            CoreCatalogProfile.objects.create(
                owner=request.user,
                category_id=category_id,
                name=name,
                base_price=base_price,
                unit=unit,
                description=description,
            )
            messages.success(request, 'Product added to your catalog.')
            return redirect('users:sellers:products')
        messages.error(request, 'Product name is required.')

    products = CoreCatalogProfile.objects.filter(owner=request.user).select_related('category').order_by('-created_at')
    categories = CategoryProfile.objects.filter(is_active=True).order_by('name')

    return render(request, 'sellers/products.html', {
        'active_tab': 'products',
        'products': products,
        'categories': categories,
        'unit_choices': CoreCatalogProfile.UnitChoices.choices,
    })


@login_required
def inventory_view(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        sku = request.POST.get('sku', '').strip()
        stock_quantity = int(request.POST.get('stock_quantity') or 0)
        low_stock_threshold = int(request.POST.get('low_stock_threshold') or 5)
        warehouse_location = request.POST.get('warehouse_location', '').strip()

        if product_id and sku:
            InventoryProfile.objects.update_or_create(
                sku=sku,
                defaults={
                    'owner': request.user,
                    'product_id': product_id,
                    'stock_quantity': stock_quantity,
                    'low_stock_threshold': low_stock_threshold,
                    'warehouse_location': warehouse_location,
                },
            )
            messages.success(request, f'Inventory updated for SKU {sku}.')
            return redirect('users:sellers:inventory')
        messages.error(request, 'Product and SKU are required.')

    products = CoreCatalogProfile.objects.filter(owner=request.user).order_by('name')
    inventories = InventoryProfile.objects.filter(owner=request.user).select_related('product').order_by('-updated_at')

    return render(request, 'sellers/inventory.html', {
        'active_tab': 'inventory',
        'products': products,
        'inventories': inventories,
    })


@login_required
def orders_view(request):
    return render(request, 'sellers/orders.html', {'active_tab': 'orders'})


@login_required
def payouts_view(request):
    return render(request, 'sellers/payouts.html', {'active_tab': 'payouts'})


@login_required
def support_view(request):
    return render(request, 'sellers/support.html', {'active_tab': 'support'})


@login_required
def profile_view(request):
    return render(request, 'sellers/profile.html', {'active_tab': 'profile'})