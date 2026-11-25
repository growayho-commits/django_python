from decimal import Decimal
import uuid

from django.db import transaction
from django.utils import timezone

from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.catalogs.core_catalogs.services.pricing_calculator_service import CataloguePricingCalculatorService
from apps.marketing_leads.carts.models.cart_profile import CartItem, CartProfile
from apps.marketing_leads.checkout_flows.models.checkout_profile import CheckoutProfile
from apps.marketing_leads.coupons_discounts.models.coupon_profile import CouponDiscountProfile
from apps.marketing_leads.orders.models.order_profile import OrderItem, OrderProfile
from apps.marketing_leads.push_notifications.models.notification_profile import PushNotificationProfile


class CartCheckoutService:
    @staticmethod
    def build_cart_summary(request):
        """Build live cart items, subtotal, coupon discount, and final total from session cart."""
        session_cart = request.session.get("hm_cart", {})
        items = []
        subtotal = Decimal("0.00")

        for cart_key, entry in session_cart.items():
            cat_id = entry.get("catalogue_id")
            catalogue = CoreCatalogProfile.objects.filter(pk=cat_id, approval_status="approved").first()
            if not catalogue:
                continue

            min_qty = catalogue.min_order_quantity or 1
            qty = max(min_qty, int(entry.get("quantity") or min_qty))
            pricing = CataloguePricingCalculatorService.calculate_price_breakdown(catalogue, quantity=qty)
            line_total = Decimal(str(pricing["final_total"]))
            unit_price = Decimal(str(pricing["unit_price"]))

            items.append({
                "cart_key": cart_key,
                "catalogue": catalogue,
                "variant_label": entry.get("variant_label", ""),
                "quantity": qty,
                "unit_price": unit_price,
                "gst_amount": Decimal(str(pricing["gst_amount"])),
                "line_total": line_total,
            })
            subtotal += line_total

        coupon_code = (request.session.get("hm_coupon") or "").strip()
        discount_amount = Decimal("0.00")
        applied_coupon = None

        if coupon_code and subtotal > 0:
            now = timezone.now()
            coupon = CouponDiscountProfile.objects.filter(
                code__iexact=coupon_code,
                is_active=True,
                valid_from__lte=now,
                valid_until__gte=now,
            ).first()
            if coupon and subtotal >= coupon.min_purchase_amount:
                applied_coupon = coupon
                if coupon.discount_type == "percentage":
                    discount_amount = (subtotal * coupon.discount_value / Decimal("100")).quantize(Decimal("0.01"))
                else:
                    discount_amount = min(subtotal, coupon.discount_value)
            else:
                request.session.pop("hm_coupon", None)

        final_total = max(Decimal("0.00"), subtotal - discount_amount)
        return {
            "items": items,
            "subtotal": subtotal.quantize(Decimal("0.01")),
            "applied_coupon": applied_coupon,
            "discount_amount": discount_amount.quantize(Decimal("0.01")),
            "final_total": final_total.quantize(Decimal("0.01")),
        }

    @staticmethod
    def sync_db_cart(user, summary):
        """Sync session cart items to CartProfile & CartItem in DB."""
        cart, _ = CartProfile.objects.get_or_create(user=user)
        cart.items.all().delete()
        for item in summary["items"]:
            CartItem.objects.create(
                cart=cart,
                product_id=item["catalogue"].sku,
                quantity=item["quantity"],
                unit_price=item["unit_price"],
            )
        return cart

    @staticmethod
    @transaction.atomic
    def place_order_from_cart(request, shipping_address, billing_address, payment_method="cod"):
        summary = CartCheckoutService.build_cart_summary(request)
        if not summary["items"]:
            raise ValueError("Your cart is empty.")

        user = request.user
        cart = CartCheckoutService.sync_db_cart(user, summary)

        CheckoutProfile.objects.create(
            user=user,
            cart_id=str(cart.id),
            status="completed",
            shipping_address=shipping_address,
            payment_method=payment_method,
            total_amount=summary["final_total"],
        )

        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        coupon = summary["applied_coupon"]
        order = OrderProfile.objects.create(
            user=user,
            order_number=order_number,
            status="pending",
            coupon_code=coupon.code if coupon else "",
            discount_amount=summary["discount_amount"],
            payment_method=payment_method,
            total_amount=summary["final_total"],
            shipping_address=shipping_address,
            billing_address=billing_address or shipping_address,
        )

        notified_owners = set()
        for item in summary["items"]:
            catalogue = item["catalogue"]
            OrderItem.objects.create(
                order=order,
                catalogue=catalogue,
                product_id=catalogue.sku,
                variant_label=item["variant_label"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                subtotal=item["line_total"],
            )
            if catalogue.owner and catalogue.owner_id != user.id and catalogue.owner_id not in notified_owners:
                PushNotificationProfile.objects.create(
                    user=catalogue.owner,
                    title=f"New Order {order.order_number}",
                    message=f"You received a new order for '{catalogue.name}' (Total: INR {order.total_amount}).",
                )
                notified_owners.add(catalogue.owner_id)

        PushNotificationProfile.objects.create(
            user=user,
            title=f"Order {order.order_number} Placed",
            message=f"Your order {order.order_number} for INR {order.total_amount} has been placed successfully.",
        )

        cart.items.all().delete()
        request.session.pop("hm_cart", None)
        request.session.pop("hm_coupon", None)
        request.session.modified = True
        return order