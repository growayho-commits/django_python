# apps/marketing_leads/checkout_flows/services/checkout_service.py

from ..models.checkout_profile import CheckoutProfile

class CheckoutService:
    @staticmethod
    def initiate_checkout(user, cart_id, total_amount):
        checkout = CheckoutProfile.objects.create(
            user=user if user and user.is_authenticated else None,
            cart_id=cart_id,
            total_amount=total_amount,
            status='initiated'
        )
        return checkout

    @staticmethod
    def update_checkout_status(checkout_id, status, payment_method=None):
        try:
            checkout = CheckoutProfile.objects.get(id=checkout_id)
            checkout.status = status
            if payment_method:
                checkout.payment_method = payment_method
            checkout.save()
            return checkout
        except CheckoutProfile.DoesNotExist:
            raise ValueError("Checkout session not found.")