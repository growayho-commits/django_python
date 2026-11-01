# apps/marketing_leads/carts/services/cart_service.py

from ..models.cart_profile import CartProfile, CartItem

class CartService:
    @staticmethod
    def get_or_create_cart(user=None, session_id=None):
        if user and user.is_authenticated:
            cart, _ = CartProfile.objects.get_or_create(user=user)
        elif session_id:
            cart, _ = CartProfile.objects.get_or_create(session_id=session_id, user__isnull=True)
        else:
            raise ValueError("Either user or session_id must be provided.")
        return cart

    @staticmethod
    def add_item_to_cart(cart, product_id, quantity, unit_price):
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity, 'unit_price': unit_price}
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item