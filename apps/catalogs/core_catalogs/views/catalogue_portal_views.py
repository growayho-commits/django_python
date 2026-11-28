from apps.catalogs.core_catalogs.services.delivery_coverage_service import CatalogueDeliveryCoverageService
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from apps.catalogs.bundles_kits.models.bundle_kit_profile import BundleKitProfile
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile
from apps.catalogs.catalog_wishlist.models.catalog_wishlist_profile import CatalogWishlistProfile
from apps.catalogs.categories.models.category_profile import CategoryProfile
from apps.catalogs.core_catalogs.forms.core_catalog_forms import CoreCatalogForm
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.catalogs.core_catalogs.selectors.core_catalog_selectors import CoreCatalogSelector
from apps.catalogs.core_catalogs.services.pricing_calculator_service import CataloguePricingCalculatorService
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile
from apps.catalogs.pricing_extras.models.pricing_extra_profile import PricingExtraProfile
from apps.catalogs.pricing_tiers.models.pricing_tier_profile import PricingTierProfile
from apps.catalogs.reviews_ratings.models.review_rating_profile import ReviewRatingProfile
from apps.catalogs.specifications.models.specification_profile import SpecificationProfile
from apps.catalogs.variants.models.variant_profile import CatalogVariantProfile
from apps.common.location_service import LocationCoverageService
from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


def _can_manage_commissions(user) -> bool:
    if user.is_superuser:
        return True
    if get_user_current_role(user) == "executive":
        exec_profile = ExecutiveProfile.objects.filter(user=user).first()
        activities = set(getattr(exec_profile, "assigned_activities", []) or [])
        return bool(activities.intersection({"catalogs", "marketing_leads"}))
    return False


def _get_related_records(catalogue, model_name_substr):
    """Safely fetch reverse-related records (variants, medias, specifications, inventories)."""
    for rel in catalogue._meta.related_objects:
        if model_name_substr in rel.related_model.__name__.lower():
            accessor = rel.get_accessor_name()
            manager = getattr(catalogue, accessor, None)
            if manager is not None:
                return list(manager.all())
    return []


@login_required
def catalogue_workspace_view(request):
    """
    Role-aware Catalogue Workspace:
    - Seller / Merchant: Create & manage their own catalogues and bulk quantity tiers
    - Superuser / Catalogs Executive: View all catalogues, approve/reject, and set commissions
    """
    current_role = (get_user_current_role(request.user) or "member").lower()
    if request.user.is_superuser:
        current_role = "superuser"

    can_commission = _can_manage_commissions(request.user)
    can_create = current_role in {"seller", "merchant", "superuser"} or can_commission

    merchant_owners = []
    seller_owners = []
    if can_commission:
        from django.contrib.auth import get_user_model
        for u in get_user_model().objects.filter(is_active=True).order_by("email"):
            r = (get_user_current_role(u) or "").lower()
            if r == "merchant":
                mp = getattr(u, "merchant_profile", None)
                name = (getattr(mp, "business_name", "") or getattr(mp, "company_name", "") or getattr(mp, "store_name", "")) if mp else ""
                label = f"{name} ({u.email})" if name else u.email
                merchant_owners.append({"user_id": u.pk, "label": label})
            elif r == "seller":
                sp = getattr(u, "seller_profile", None)
                name = (getattr(sp, "business_name", "") or getattr(sp, "store_name", "") or getattr(sp, "shop_name", "")) if sp else ""
                label = f"{name} ({u.email})" if name else u.email
                seller_owners.append({"user_id": u.pk, "label": label})

    if request.method == "POST" and can_create:
        form = CoreCatalogForm(request.POST)
        if form.is_valid():
            catalogue = form.save(commit=False)
            selected_owner_id = request.POST.get("owner_id", "").strip()
            if can_commission and selected_owner_id:
                try:
                    from django.contrib.auth import get_user_model
                    sel_user = get_user_model().objects.get(pk=selected_owner_id)
                    catalogue.owner = sel_user
                    sel_role = (get_user_current_role(sel_user) or "").lower()
                    if sel_role == "merchant":
                        catalogue.trade_channel = "b2b"
                    elif sel_role == "seller":
                        catalogue.trade_channel = "b2c"
                except Exception:
                    catalogue.owner = request.user
            else:
                catalogue.owner = request.user
            raw_locations = request.POST.get("delivery_locations_text", "")
            catalogue.delivery_locations = [
                loc.strip() for loc in raw_locations.split(",") if loc.strip()
            ]
            if request.user.is_superuser:
                catalogue.approval_status = "approved"
            else:
                catalogue.approval_status = "pending"
            catalogue.save()
            messages.success(request, f"Catalogue '{catalogue.name}' saved successfully.")
            return redirect("catalogs:core_catalogs:catalogue_workspace")
    else:
        form = CoreCatalogForm()

    if can_commission:
        catalogues = CoreCatalogSelector.get_all_catalogues()
    else:
        catalogues = CoreCatalogSelector.get_owner_catalogues(request.user)

    context = {
        "current_role": current_role,
        "can_create": can_create,
        "can_commission": can_commission,
        "merchant_owners": merchant_owners,
        "seller_owners": seller_owners,
        "india_locations": __import__("apps.catalogs.core_catalogs.services.india_locations", fromlist=["INDIA_STATE_DISTRICTS"]).INDIA_STATE_DISTRICTS,
        "form": form,
        "catalogues": catalogues,
    }
    return render(request, "catalogs/catalogue_workspace.html", context)


@login_required
def manage_catalogue_details_view(request, pk):
    """Manage Inventory, Variants, Media Gallery, and Specifications for a Catalogue."""
    catalogue = get_object_or_404(CoreCatalogProfile, pk=pk)
    can_commission = _can_manage_commissions(request.user)
    is_owner = catalogue.owner_id == request.user.id

    if not (can_commission or is_owner):
        messages.error(request, "You do not have permission to edit details for this catalogue.")
        return redirect("catalogs:core_catalogs:catalogue_workspace")

    inventory, _ = InventoryProfile.objects.get_or_create(
        catalogue=catalogue,
        defaults={"sku": catalogue.sku, "owner": catalogue.owner or request.user},
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "save_inventory":
            inventory.stock_quantity = max(0, int(request.POST.get("stock_quantity") or 0))
            inventory.reserved_quantity = max(0, int(request.POST.get("reserved_quantity") or 0))
            inventory.low_stock_threshold = max(0, int(request.POST.get("low_stock_threshold") or 5))
            inventory.warehouse_location = request.POST.get("warehouse_location", "").strip()
            inventory.save()
            messages.success(request, f"Inventory updated for '{catalogue.name}'.")

        elif action == "add_variant":
            variant_name = request.POST.get("variant_name", "").strip()
            variant_sku = request.POST.get("variant_sku", "").strip() or f"{catalogue.sku}-{uuid.uuid4().hex[:4].upper()}"
            if variant_name:
                try:
                    CatalogVariantProfile.objects.create(
                        catalogue=catalogue,
                        variant_name=variant_name,
                        sku=variant_sku,
                        price_adjustment=request.POST.get("price_adjustment") or 0,
                        stock_quantity=max(0, int(request.POST.get("variant_stock") or 0)),
                        is_active=True,
                    )
                    messages.success(request, f"Variant '{variant_name}' added.")
                except IntegrityError:
                    messages.error(request, f"Variant SKU '{variant_sku}' already exists.")

        elif action == "delete_variant":
            CatalogVariantProfile.objects.filter(pk=request.POST.get("item_id"), catalogue=catalogue).delete()
            messages.info(request, "Variant removed.")

        elif action == "add_media":
            media_url = request.POST.get("media_url", "").strip()
            if media_url:
                is_primary = bool(request.POST.get("is_primary"))
                if is_primary:
                    CatalogMediaProfile.objects.filter(catalogue=catalogue, is_primary=True).update(is_primary=False)
                CatalogMediaProfile.objects.create(
                    catalogue=catalogue,
                    media_type=request.POST.get("media_type", "image"),
                    media_url=media_url,
                    alt_text=request.POST.get("alt_text", "").strip() or catalogue.name,
                    is_primary=is_primary,
                    display_order=int(request.POST.get("display_order") or 0),
                )
                messages.success(request, "Media item added.")

        elif action == "delete_media":
            CatalogMediaProfile.objects.filter(pk=request.POST.get("item_id"), catalogue=catalogue).delete()
            messages.info(request, "Media item removed.")

        elif action == "add_specification":
            spec_key = request.POST.get("spec_key", "").strip()
            spec_value = request.POST.get("spec_value", "").strip()
            if spec_key and spec_value:
                SpecificationProfile.objects.create(
                    catalogue=catalogue,
                    spec_group=request.POST.get("spec_group", "General").strip() or "General",
                    spec_key=spec_key,
                    spec_value=spec_value,
                    display_order=int(request.POST.get("display_order") or 0),
                )
                messages.success(request, f"Specification '{spec_key}' added.")

        elif action == "delete_specification":
            SpecificationProfile.objects.filter(pk=request.POST.get("item_id"), catalogue=catalogue).delete()
            messages.info(request, "Specification removed.")

        return redirect("catalogs:core_catalogs:manage_catalogue_details", pk=catalogue.pk)

    return render(request, "catalogs/manage_catalogue_details.html", {
        "catalogue": catalogue,
        "inventory": inventory,
        "variants": catalogue.variants.all().order_by("variant_name"),
        "medias": catalogue.medias.all().order_by("display_order", "-is_primary"),
        "specifications": catalogue.specifications.all().order_by("display_order", "spec_group"),
    })


@login_required
def manage_categories_view(request):
    """Create and toggle active/inactive Catalogue Categories."""
    can_manage = _can_manage_commissions(request.user) or (
        (get_user_current_role(request.user) or "").lower() in {"seller", "merchant", "superuser"}
    )
    if not can_manage:
        messages.error(request, "Permission denied.")
        return redirect("catalogs:core_catalogs:catalogue_marketplace")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_category":
            name = request.POST.get("name", "").strip()
            description = request.POST.get("description", "").strip()
            if name:
                base_slug = slugify(name) or f"cat-{uuid.uuid4().hex[:6]}"
                unique_slug = base_slug
                counter = 1
                while CategoryProfile.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{base_slug}-{counter}"
                    counter += 1
                try:
                    CategoryProfile.objects.create(name=name, slug=unique_slug, description=description, is_active=True)
                    messages.success(request, f"Category '{name}' created.")
                except IntegrityError:
                    messages.error(request, f"Category '{name}' already exists.")

        elif action == "toggle_category":
            cat = get_object_or_404(CategoryProfile, pk=request.POST.get("category_id"))
            cat.is_active = not cat.is_active
            cat.save(update_fields=["is_active"])
            messages.info(request, f"Category '{cat.name}' updated.")

        return redirect("catalogs:core_catalogs:manage_categories")

    categories = CategoryProfile.objects.all().order_by("name")
    return render(request, "catalogs/manage_categories.html", {"categories": categories})


@login_required
def manage_bundles_view(request):
    """Create and manage Bundles / Kits combining multiple catalogues."""
    can_commission = _can_manage_commissions(request.user)
    current_role = (get_user_current_role(request.user) or "member").lower()
    if request.user.is_superuser:
        current_role = "superuser"

    if current_role not in {"seller", "merchant", "superuser"} and not can_commission:
        messages.error(request, "Permission denied.")
        return redirect("catalogs:core_catalogs:catalogue_marketplace")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_bundle":
            bundle_name = request.POST.get("bundle_name", "").strip()
            bundle_sku = request.POST.get("bundle_sku", "").strip() or f"BND-{uuid.uuid4().hex[:6].upper()}"
            bundle_price = request.POST.get("bundle_price") or 0
            description = request.POST.get("description", "").strip()
            catalogue_ids = request.POST.getlist("catalogues")

            if bundle_name:
                try:
                    bundle = BundleKitProfile.objects.create(
                        owner=request.user,
                        bundle_name=bundle_name,
                        bundle_sku=bundle_sku,
                        bundle_price=bundle_price,
                        description=description,
                        is_active=True,
                    )
                    if catalogue_ids:
                        bundle.catalogues.set(CoreCatalogProfile.objects.filter(id__in=catalogue_ids))
                    messages.success(request, f"Bundle '{bundle_name}' created successfully.")
                except IntegrityError:
                    messages.error(request, "Bundle name or SKU already exists.")

        elif action == "toggle_bundle":
            bundle = get_object_or_404(BundleKitProfile, pk=request.POST.get("bundle_id"))
            if can_commission or bundle.owner_id == request.user.id:
                bundle.is_active = not bundle.is_active
                bundle.save(update_fields=["is_active"])
                messages.info(request, f"Bundle '{bundle.bundle_name}' status updated.")

        return redirect("catalogs:core_catalogs:manage_bundles")

    if can_commission:
        bundles = BundleKitProfile.objects.prefetch_related("catalogues").order_by("-created_at")
        available_catalogues = CoreCatalogProfile.objects.filter(is_active=True).order_by("name")
    else:
        bundles = BundleKitProfile.objects.filter(owner=request.user).prefetch_related("catalogues").order_by("-created_at")
        available_catalogues = CoreCatalogProfile.objects.filter(owner=request.user, is_active=True).order_by("name")

    return render(request, "catalogs/manage_bundles.html", {
        "bundles": bundles,
        "available_catalogues": available_catalogues,
    })


@login_required
def my_wishlist_view(request):
    """Display all catalogues wishlisted by the current user."""
    items = (
        CatalogWishlistProfile.objects.filter(user=request.user, catalogue__isnull=False)
        .select_related("catalogue")
        .order_by("-created_at")
    )
    wishlist_cards = [
        {
            "wishlist": item,
            "catalogue": item.catalogue,
            "pricing": CataloguePricingCalculatorService.calculate_price_breakdown(
                item.catalogue, quantity=item.catalogue.min_order_quantity or 1
            ),
        }
        for item in items
    ]
    return render(request, "catalogs/my_wishlist.html", {"wishlist_cards": wishlist_cards})


@login_required
def configure_catalogue_pricing_view(request, pk):
    """Allow Superuser (or authorized Executive) to set Commissions and Seller/Merchant to add Bulk Tiers."""
    catalogue = get_object_or_404(CoreCatalogProfile, pk=pk)
    can_commission = _can_manage_commissions(request.user)
    is_owner = catalogue.owner_id == request.user.id

    if not (can_commission or is_owner):
        messages.error(request, "You do not have permission to configure pricing for this catalogue.")
        return redirect("catalogs:core_catalogs:catalogue_workspace")

    commission_cfg, _ = PricingExtraProfile.objects.get_or_create(catalogue=catalogue)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "save_commissions" and can_commission:
            commission_cfg.configured_by = request.user
            commission_cfg.superuser_commission_mode = request.POST.get("superuser_commission_mode", "percentage")
            commission_cfg.superuser_commission_value = request.POST.get("superuser_commission_value") or 0
            commission_cfg.executive_commission_mode = request.POST.get("executive_commission_mode", "percentage")
            commission_cfg.executive_commission_value = request.POST.get("executive_commission_value") or 0
            commission_cfg.seller_commission_mode = request.POST.get("seller_commission_mode", "percentage")
            commission_cfg.seller_commission_value = request.POST.get("seller_commission_value") or 0
            commission_cfg.extra_handling_charge = request.POST.get("extra_handling_charge") or 0
            commission_cfg.estimated_delivery_charge = request.POST.get("estimated_delivery_charge") or 0
            commission_cfg.save()
            messages.success(request, f"Commission & pricing rules updated for '{catalogue.name}'.")

        elif action == "add_bulk_tier" and (is_owner or can_commission):
            PricingTierProfile.objects.create(
                catalogue=catalogue,
                tier_name=request.POST.get("tier_name", "Bulk Tier").strip() or "Bulk Tier",
                min_quantity=int(request.POST.get("min_quantity") or 1),
                max_quantity=int(request.POST["max_quantity"]) if request.POST.get("max_quantity") else None,
                adjustment_type=request.POST.get("adjustment_type", "fixed_price"),
                tier_value=request.POST.get("tier_value") or 0,
            )
            messages.success(request, f"Bulk quantity tier added to '{catalogue.name}'.")

        return redirect("catalogs:core_catalogs:configure_catalogue_pricing", pk=catalogue.pk)

    sample_qty = int(request.GET.get("qty", 1) or 1)
    breakdown = CataloguePricingCalculatorService.calculate_price_breakdown(catalogue, quantity=sample_qty)

    return render(request, "catalogs/configure_catalogue_pricing.html", {
        "catalogue": catalogue,
        "commission_cfg": commission_cfg,
        "tiers": catalogue.pricing_tiers.all(),
        "breakdown": breakdown,
        "can_commission": can_commission,
        "is_owner": is_owner,
    })


@login_required
def approve_catalogue_view(request, pk):
    """Approve or reject a catalogue (Superuser / authorized Executive)."""
    if not _can_manage_commissions(request.user):
        messages.error(request, "Permission denied.")
        return redirect("catalogs:core_catalogs:catalogue_workspace")

    catalogue = get_object_or_404(CoreCatalogProfile, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("approval_status")
        if new_status in {"approved", "rejected", "pending", "draft"}:
            catalogue.approval_status = new_status
            catalogue.save(update_fields=["approval_status"])
            messages.success(request, f"Catalogue '{catalogue.name}' status set to {new_status.title()}.")
    return redirect("catalogs:core_catalogs:catalogue_workspace")


@login_required
def catalogue_marketplace_view(request):
    """
    High-Impression Amazon/Flipkart/Alibaba Storefront:
    - Guest, Member, Executive: Strictly B2C Seller catalogues only.
    - Seller, Merchant, Superuser: Both B2B Merchant & B2C Seller catalogues.
    - 3-Tier Arrangement:
      1) Assigned Seller/Partner matching active pincode
      2) Other Suppliers available in active pincode
      3) Explore All Other Catalogues
    """
    current_role = (get_user_current_role(request.user) or "member").lower()
    if request.user.is_superuser:
        current_role = "superuser"

    if current_role in ("member", "executive"):
        trade_channel = "b2c"
    else:
        default_channel = "b2b" if current_role == "seller" else "all"
        trade_channel = request.GET.get("channel", default_channel).strip().lower()

    category_id = request.GET.get("category") or None
    search_query = request.GET.get("q", "").strip()
    pincode = request.GET.get("pincode", "").strip() or None
    taluk = request.GET.get("taluk", "").strip() or None
    district = request.GET.get("district", "").strip() or None
    state = request.GET.get("state", "").strip() or None

    active_address_label = ""
    if current_role == "member" and not any([pincode, taluk, district, state]):
        try:
            from apps.users.superusers.models.address import UserAddress
            addr = (
                UserAddress.objects.filter(user=request.user, address_type="SHIPPING", is_default=True).first()
                or UserAddress.objects.filter(user=request.user, address_type="SHIPPING").order_by("-updated_at", "-id").first()
                or UserAddress.objects.filter(user=request.user, is_default=True).first()
                or UserAddress.objects.filter(user=request.user).order_by("-updated_at", "-id").first()
            )
            if addr:
                pincode = addr.pincode or None
                district = addr.city or None
                state = addr.state or None
                active_address_label = f"{addr.city} - {addr.pincode}" if addr.pincode else addr.city
        except Exception:
            pass

    if not any([pincode, taluk, district, state]):
        cookie_pin = (request.COOKIES.get("hm_pincode") or "").strip()
        if cookie_pin.isdigit() and len(cookie_pin) == 6:
            pincode = cookie_pin
            active_address_label = f"Pincode {cookie_pin}"

    # Base approved queryset (filtered by channel, category, search ? WITHOUT location drop so Row 3 can show Explore All)
    all_matching_qs = CoreCatalogSelector.get_approved_marketplace_catalogues(
        category_id=category_id,
        search_query=search_query,
        trade_channel=trade_channel if trade_channel in {"b2b", "b2c"} else None,
    )
    if request.user.is_authenticated and not request.user.is_superuser:
        all_matching_qs = all_matching_qs.exclude(owner=request.user)

    assigned_owner_ids = set()
    if current_role == "member":
        try:
            mp = getattr(request.user, "member_profile", None)
            if mp and mp.assigned_seller and mp.assigned_seller.user_id:
                assigned_owner_ids.add(mp.assigned_seller.user_id)
        except Exception:
            pass
    elif current_role == "executive":
        try:
            from apps.users.sellers.models.seller_profile import SellerProfile
            assigned_owner_ids.update(
                SellerProfile.objects.filter(assigned_executive=request.user).values_list("user_id", flat=True)
            )
        except Exception:
            pass

    wishlisted_ids = set(
        CatalogWishlistProfile.objects.filter(user=request.user, catalogue__isnull=False)
        .values_list("catalogue_id", flat=True)
    )

    has_loc = any([pincode, taluk, district, state])
    tier1_assigned = []
    tier2_local = []
    tier3_explore = []

    for cat in all_matching_qs.order_by("-id"):
        supplier_role = get_user_current_role(cat.owner).title() if cat.owner else "Platform"
        is_assigned = cat.owner_id in assigned_owner_ids
        is_local = True if not has_loc else CatalogueDeliveryCoverageService.is_deliverable_to(
            cat, pincode=pincode, taluk=taluk, district=district, state=state
        )
        mrp = float(cat.mrp_price or 0)
        pricing = CataloguePricingCalculatorService.calculate_price_breakdown(
            cat, quantity=cat.min_order_quantity or 1
        )
        final_p = float(pricing.get("final_total") or 0)
        discount_pct = int(round(((mrp - final_p) / mrp) * 100)) if mrp > final_p > 0 else 0

        card = {
            "catalogue": cat,
            "supplier_role": supplier_role,
            "is_assigned": is_assigned,
            "is_local": is_local,
            "is_wishlisted": cat.id in wishlisted_ids,
            "pricing": pricing,
            "discount_pct": discount_pct,
        }
        if is_assigned and is_local:
            tier1_assigned.append(card)
        elif is_local:
            tier2_local.append(card)
        else:
            tier3_explore.append(card)

    catalogue_cards = tier1_assigned + tier2_local + tier3_explore
    session_cart = request.session.get("hm_cart", {})
    cart_count = sum(item.get("quantity", 0) for item in session_cart.values())

    active_campaigns = []
    active_coupons = []
    try:
        from apps.marketing_leads.ads_campaigns.models.campaign_profile import AdsCampaignProfile
        active_campaigns = list(AdsCampaignProfile.objects.filter(is_active=True).order_by("-id")[:4])
    except Exception:
        pass
    try:
        from apps.marketing_leads.coupons_discounts.models.coupon_profile import CouponDiscountProfile
        active_coupons = list(CouponDiscountProfile.objects.filter(is_active=True).order_by("-id")[:4])
    except Exception:
        pass

    quick_categories = list(
        CategoryProfile.objects.filter(is_active=True, parent__isnull=True).order_by("name")[:12]
    ) or list(CategoryProfile.objects.filter(is_active=True).order_by("name")[:12])

    return render(request, "catalogs/catalogue_marketplace.html", {
        "current_role": current_role,
        "catalogue_cards": catalogue_cards,
        "tier1_assigned": tier1_assigned,
        "tier2_local": tier2_local,
        "tier3_explore": tier3_explore,
        "categories": CategoryProfile.objects.filter(is_active=True).order_by("name")[:50],
        "quick_categories": quick_categories,
        "active_campaigns": active_campaigns,
        "active_coupons": active_coupons,
        "cart_count": cart_count,
        "active_address_label": active_address_label,
        "filter_open": any([request.GET.get("category"), request.GET.get("pincode"), request.GET.get("taluk"), request.GET.get("district"), request.GET.get("state")]),
        "filters": {
            "channel": trade_channel,
            "category": category_id,
            "q": search_query,
            "pincode": pincode or "",
            "taluk": taluk or "",
            "district": district or "",
            "state": state or "",
        },
    })


@login_required
def catalogue_detail_view(request, pk):
    """
    Full Buyer-Facing Catalogue Detail Page:
    - Media Gallery, Variants, Specifications, Bulk Pricing Tiers
    - Live Quantity Price Breakdown
    - Location / Pincode Delivery Coverage Check via apps/common/location_service.py
    - Verified Reviews & Ratings + Add to Wishlist + Add to Cart
    """
    catalogue = get_object_or_404(CoreCatalogProfile, pk=pk)
    if catalogue.approval_status != "approved" and catalogue.owner_id != request.user.id and not _can_manage_commissions(request.user):
        messages.error(request, "This catalogue is not yet approved for marketplace viewing.")
        return redirect("catalogs:core_catalogs:catalogue_marketplace")

    min_qty = catalogue.min_order_quantity or 1
    try:
        selected_qty = max(min_qty, int(request.GET.get("qty", min_qty) or min_qty))
    except ValueError:
        selected_qty = min_qty

    breakdown = CataloguePricingCalculatorService.calculate_price_breakdown(catalogue, quantity=selected_qty)
    tiers = list(catalogue.pricing_tiers.all().order_by("min_quantity"))
    variants = _get_related_records(catalogue, "variant")
    medias = _get_related_records(catalogue, "media")
    specifications = _get_related_records(catalogue, "specification")
    inventories = _get_related_records(catalogue, "inventory")

    check_pincode = request.GET.get("check_pincode", "").strip() or None
    check_taluk = request.GET.get("check_taluk", "").strip() or None
    check_district = request.GET.get("check_district", "").strip() or None
    check_state = request.GET.get("check_state", "").strip() or None

    delivery_checked = any([check_pincode, check_taluk, check_district, check_state])
    is_deliverable = None
    if delivery_checked:
        is_deliverable = LocationCoverageService.is_location_covered(
            scope=catalogue.delivery_scope,
            locations=catalogue.delivery_locations,
            pincode=check_pincode,
            taluk=check_taluk,
            district=check_district,
            state=check_state,
        )

    reviews_qs = ReviewRatingProfile.objects.filter(catalogue=catalogue, is_approved=True).order_by("-created_at")
    avg_rating = reviews_qs.aggregate(avg=Avg("rating_score"))["avg"] or 0
    is_wishlisted = CatalogWishlistProfile.objects.filter(user=request.user, catalogue=catalogue).exists()
    supplier_role = get_user_current_role(catalogue.owner).title() if catalogue.owner else "Platform"

    return render(request, "catalogs/catalogue_detail.html", {
        "catalogue": catalogue,
        "supplier_role": supplier_role,
        "selected_qty": selected_qty,
        "breakdown": breakdown,
        "tiers": tiers,
        "variants": variants,
        "medias": medias,
        "specifications": specifications,
        "inventories": inventories,
        "reviews": reviews_qs,
        "avg_rating": round(avg_rating, 1),
        "review_count": reviews_qs.count(),
        "is_wishlisted": is_wishlisted,
        "delivery_checked": delivery_checked,
        "is_deliverable": is_deliverable,
        "check_location": {
            "pincode": check_pincode or "",
            "taluk": check_taluk or "",
            "district": check_district or "",
            "state": check_state or "",
        },
    })


@login_required
def toggle_wishlist_view(request, pk):
    """Add or remove a catalogue from the current user's wishlist."""
    catalogue = get_object_or_404(CoreCatalogProfile, pk=pk)
    if request.method == "POST":
        existing = CatalogWishlistProfile.objects.filter(user=request.user, catalogue=catalogue).first()
        if existing:
            existing.delete()
            messages.info(request, f"Removed '{catalogue.name}' from your wishlist.")
        else:
            CatalogWishlistProfile.objects.create(
                user=request.user,
                catalogue=catalogue,
                user_identifier=request.user.email,
                product_sku=catalogue.sku,
            )
            messages.success(request, f"Added '{catalogue.name}' to your wishlist.")

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER")
    if next_url:
        return redirect(next_url)
    return redirect("catalogs:core_catalogs:catalogue_detail", pk=catalogue.pk)


@login_required
def submit_catalogue_review_view(request, pk):
    """Submit a 1-5 star rating and review for a catalogue."""
    catalogue = get_object_or_404(CoreCatalogProfile, pk=pk)
    if request.method == "POST":
        try:
            score = int(request.POST.get("rating_score", 5))
        except ValueError:
            score = 5
        score = max(1, min(5, score))
        comment = request.POST.get("comment", "").strip()
        reviewer_name = request.user.get_full_name() or request.user.email

        ReviewRatingProfile.objects.create(
            catalogue=catalogue,
            reviewer=request.user,
            product_sku=catalogue.sku,
            reviewer_name=reviewer_name,
            rating_score=score,
            comment=comment,
            is_approved=True,
        )
        messages.success(request, f"Thank you! Your {score}-star review for '{catalogue.name}' has been posted.")
    return redirect("catalogs:core_catalogs:catalogue_detail", pk=catalogue.pk)


@login_required
def add_to_cart_session_view(request, pk):
    """Session-backed Add to Cart ready for Phase C Checkout integration."""
    catalogue = get_object_or_404(CoreCatalogProfile, pk=pk, approval_status="approved")
    if request.method == "POST":
        min_qty = catalogue.min_order_quantity or 1
        try:
            qty = max(min_qty, int(request.POST.get("quantity", min_qty) or min_qty))
        except ValueError:
            qty = min_qty
        variant_label = request.POST.get("variant_label", "").strip()
        cart_key = f"{catalogue.id}:{variant_label}" if variant_label else str(catalogue.id)

        cart = request.session.get("hm_cart", {})
        current_qty = cart.get(cart_key, {}).get("quantity", 0)
        cart[cart_key] = {
            "catalogue_id": catalogue.id,
            "catalogue_name": catalogue.name,
            "sku": catalogue.sku,
            "variant_label": variant_label,
            "quantity": current_qty + qty,
        }
        request.session["hm_cart"] = cart
        request.session.modified = True
        messages.success(request, f"Added {qty} x '{catalogue.name}' to your cart.")
    return redirect("catalogs:core_catalogs:catalogue_detail", pk=catalogue.pk)

def category_autocomplete_api(request):
    from django.http import JsonResponse
    from apps.catalogs.categories.models.category_profile import CategoryProfile
    q = request.GET.get("q", "").strip()
    qs = CategoryProfile.objects.filter(is_active=True)
    if q:
        qs = qs.filter(name__icontains=q)
    results = [{"id": str(c["id"]), "name": c["name"]} for c in qs.order_by("name").values("id", "name")[:35]]
    return JsonResponse({"results": results})
