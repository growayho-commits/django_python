import razorpay
from django.conf import settings
from apps.finances.payment_gateways.models import PaymentGatewayConfig[cite: 1]
from apps.marketing_leads.orders.models import OrderProfile[cite: 1]

class EscrowPaymentService:
    def __init__(self):
        self.client = razorpay.Client(
            auth=(
                getattr(settings, 'RAZORPAY_KEY_ID', ''),
                getattr(settings, 'RAZORPAY_KEY_SECRET', '')
            )
        )

    def create_b2b_escrow_order(self, order_id, credit_period_days=30):
        order = OrderProfile.objects.get(id=order_id)
        amount_in_paisa = int(order.total_amount * 100)
        
        data = {
            "amount": amount_in_paisa,
            "currency": "INR",
            "receipt": f"order_rcpt_{order.id}",
            "notes": {
                "order_id": str(order.id),
                "escrow": "TRUE",
                "credit_period_days": str(credit_period_days)
            }
        }
        razorpay_order = self.client.order.create(data=data)
        return razorpay_order

    def release_escrow_funds(self, razorpay_payment_id):
        # Escrow நிதியை விற்பனையாளருக்கு விடுவிக்கும் செயல்பாடு
        capture_response = self.client.payment.capture(razorpay_payment_id)
        return capture_response


# apps/finances/payment_gateways/services/escrow_service.py
from django.core.exceptions import ValidationError
from apps.marketing_leads.orders.models import OrderProfile

class EscrowPaymentService:
    @staticmethod
    def hold_payment_in_escrow(order_id, amount):
        order = OrderProfile.objects.filter(id=order_id).first()
        if not order:
            raise ValidationError("குறிப்பிட்ட ஆர்டர் கிடைக்கவில்லை.")
        
        order.payment_status = "ESCROW_HELD"
        order.save()
        return {"status": "HELD", "order_id": order_id, "amount": amount}

    @staticmethod
    def release_escrow_to_seller(order_id):
        order = OrderProfile.objects.filter(id=order_id).first()
        if not order:
            raise ValidationError("குறிப்பிட்ட ஆர்டர் கிடைக்கவில்லை.")
        
        order.payment_status = "RELEASED_TO_SELLER"
        order.save()
        return {"status": "RELEASED", "order_id": order_id}