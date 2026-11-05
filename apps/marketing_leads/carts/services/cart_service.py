from django.db import transaction
from apps.marketing_leads.carts.models import CartProfile
from apps.marketing_leads.orders.models import OrderProfile, OrderItem

class CartCheckoutService:
    @staticmethod
    @transaction.atomic
    def checkout_cart(user, shipping_address, billing_address):
        try:
            # பயனரின் கார்ட்டைப் பெறுதல்
            cart = CartProfile.objects.get(user=user)
            cart_items = cart.cartitem_set.all()

            if not cart_items.exists():
                raise ValueError("கார்ட்டில் எந்தப் பொருட்களும் இல்லை.")

            # மொத்த தொகையைக் கணக்கிடுதல்
            total_amount = 0
            for item in cart_items:
                # தயாரிப்பின் விலை மற்றும் அளவைக் கொண்டு மொத்தத் தொகைக் கணக்கு
                item_total = item.product.price * item.quantity if hasattr(item.product, 'price') else 0
                total_amount += item_total

            # புதிய ஆர்டரை உருவாக்குதல் (OrderProfile)
            order = OrderProfile.objects.create(
                user=user,
                status='PENDING',
                total_amount=total_amount,
                shipping_address=shipping_address,
                billing_address=billing_address
            )

            # கார்ட் பொருட்களை ஆர்டர் ஐட்டம்களாக மாற்றுதல்
            for item in cart_items:
                item_price = item.product.price if hasattr(item.product, 'price') else 0
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item_price
                )

            # ஆர்டர் வெற்றிகரமாக உருவாக்கப்பட்ட பிறகு கார்ட்டை காலியாக்குதல்
            cart_items.delete()

            return order

        except CartProfile.DoesNotExist:
            raise ValueError("பயனருக்கான கார்ட் கண்டுபிடிக்கப்படவில்லை.")