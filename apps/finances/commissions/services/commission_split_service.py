from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.catalogs.pricing_extras.models.pricing_extra_profile import PricingExtraProfile
from apps.finances.commissions.models.commission_profile import CommissionProfile

CoreUser = get_user_model()


class CommissionSplitService:
    @staticmethod
    def _compute_part(base_amount: Decimal, mode: str, value: Decimal) -> Decimal:
        if not value or value <= 0:
            return Decimal("0.00")
        if mode == "percentage":
            return (base_amount * value / Decimal("100")).quantize(Decimal("0.01"))
        return Decimal(str(value)).quantize(Decimal("0.01"))

    @staticmethod
    @transaction.atomic
    def generate_splits_for_order(order):
        """
        Auto-split commissions for Superuser, Executive, and Seller
        based on PricingExtraProfile rules on each OrderItem.catalogue.
        """
        if CommissionProfile.objects.filter(order_id=order.order_number).exists():
            return list(CommissionProfile.objects.filter(order_id=order.order_number))

        superuser_user = CoreUser.objects.filter(is_superuser=True).order_by("id").first()
        created_records = []

        for item in order.items.select_related("catalogue__owner").all():
            catalogue = item.catalogue
            if not catalogue:
                continue

            cfg = PricingExtraProfile.objects.filter(catalogue=catalogue).first()
            if not cfg:
                continue

            line_subtotal = Decimal(str(item.subtotal))
            owner = catalogue.owner or superuser_user

            # 1. Superuser / Platform Commission
            su_amt = CommissionSplitService._compute_part(
                line_subtotal, cfg.superuser_commission_mode, cfg.superuser_commission_value
            )
            if su_amt > 0 and superuser_user:
                created_records.append(CommissionProfile.objects.create(
                    vendor=superuser_user,
                    order_ref=order,
                    order_id=order.order_number,
                    recipient_role="superuser",
                    total_amount=line_subtotal,
                    commission_percentage=cfg.superuser_commission_value if cfg.superuser_commission_mode == "percentage" else Decimal("0.00"),
                    commission_amount=su_amt,
                    payout_status="approved",
                ))

            # 2. Executive Commission
            exec_amt = CommissionSplitService._compute_part(
                line_subtotal, cfg.executive_commission_mode, cfg.executive_commission_value
            )
            exec_user = None
            if owner:
                if hasattr(owner, "seller_profile") and owner.seller_profile.assigned_executive:
                    exec_user = owner.seller_profile.assigned_executive.user
                elif hasattr(owner, "merchant_profile") and owner.merchant_profile.assigned_executive:
                    exec_user = owner.merchant_profile.assigned_executive.user
            if exec_amt > 0 and (exec_user or superuser_user):
                created_records.append(CommissionProfile.objects.create(
                    vendor=exec_user or superuser_user,
                    order_ref=order,
                    order_id=order.order_number,
                    recipient_role="executive",
                    total_amount=line_subtotal,
                    commission_percentage=cfg.executive_commission_value if cfg.executive_commission_mode == "percentage" else Decimal("0.00"),
                    commission_amount=exec_amt,
                    payout_status="pending",
                ))

            # 3. Seller / Owner Commission
            sel_amt = CommissionSplitService._compute_part(
                line_subtotal, cfg.seller_commission_mode, cfg.seller_commission_value
            )
            if sel_amt > 0 and owner:
                created_records.append(CommissionProfile.objects.create(
                    vendor=owner,
                    order_ref=order,
                    order_id=order.order_number,
                    recipient_role="seller",
                    total_amount=line_subtotal,
                    commission_percentage=cfg.seller_commission_value if cfg.seller_commission_mode == "percentage" else Decimal("0.00"),
                    commission_amount=sel_amt,
                    payout_status="pending",
                ))

        return created_records