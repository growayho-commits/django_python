import uuid

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.finances.commissions.services.commission_split_service import CommissionSplitService
from apps.finances.payment_gateways.models.gateway_profile import EscrowTransaction
from apps.marketing_leads.orders.models.order_profile import OrderProfile


class EscrowPaymentService:
    @staticmethod
    @transaction.atomic
    def hold_payment_in_escrow(order_id, gateway_name="Escrow / UPI"):
        order = OrderProfile.objects.filter(pk=order_id).first()
        if not order:
            raise ValidationError("Order not found.")

        escrow, created = EscrowTransaction.objects.get_or_create(
            order=order,
            defaults={
                "buyer": order.user,
                "amount": order.total_amount,
                "gateway_name": gateway_name,
                "gateway_reference": f"ESC-{uuid.uuid4().hex[:10].upper()}",
                "escrow_status": "held",
            },
        )
        if not created and escrow.escrow_status != "held":
            escrow.escrow_status = "held"
            escrow.save(update_fields=["escrow_status"])

        if order.status == "pending":
            order.status = "confirmed"
            order.save(update_fields=["status"])
        return escrow

    @staticmethod
    @transaction.atomic
    def release_escrow_to_seller(order_id):
        order = OrderProfile.objects.filter(pk=order_id).first()
        if not order:
            raise ValidationError("Order not found.")

        escrow = getattr(order, "escrow_transaction", None)
        if not escrow:
            escrow = EscrowPaymentService.hold_payment_in_escrow(order.pk)

        escrow.escrow_status = "released"
        escrow.released_at = timezone.now()
        escrow.save(update_fields=["escrow_status", "released_at"])

        splits = CommissionSplitService.generate_splits_for_order(order)
        return {"escrow": escrow, "splits": splits}