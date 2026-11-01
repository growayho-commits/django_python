# apps/marketing_leads/orders/services/order_service.py

import uuid
from ..models.order_profile import OrderProfile, OrderItem

class OrderService:
    @staticmethod
    def create_order(user, shipping_address, billing_address, items_data):
        order_number = "ORD-" + uuid.uuid4().hex[:8].upper()
        total_amount = sum(item['quantity'] * item['unit_price'] for item in items_data)
        
        order = OrderProfile.objects.create(
            user=user,
            order_number=order_number,
            total_amount=total_amount,
            shipping_address=shipping_address,
            billing_address=billing_address,
            status='pending'
        )

        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                subtotal=item['quantity'] * item['unit_price']
            )
            
        return order