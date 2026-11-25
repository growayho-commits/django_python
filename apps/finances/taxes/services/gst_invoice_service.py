from decimal import Decimal
import uuid

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.finances.commissions.models.commission_profile import CommissionProfile
from apps.finances.taxes.models.tax_profile import InHouseGSTInvoice
from apps.users.superusers.services.role_request_service import get_user_current_role

CoreUser = get_user_model()


class InHouseGSTInvoiceService:
    @staticmethod
    def _split_gst(taxable_amount: Decimal, gst_rate: Decimal, is_inter_state: bool = False):
        total_gst = (taxable_amount * gst_rate / Decimal("100")).quantize(Decimal("0.01"))
        if is_inter_state:
            return Decimal("0.00"), Decimal("0.00"), total_gst, total_gst
        half = (total_gst / Decimal("2")).quantize(Decimal("0.01"))
        return half, total_gst - half, Decimal("0.00"), total_gst

    @staticmethod
    def _get_user_gstin(user) -> str:
        if not user:
            return "UNREGISTERED"
        bp = getattr(user, "business_profile", None)
        if bp and getattr(bp, "gst_number", None):
            return bp.gst_number
        return "UNREGISTERED"

    @staticmethod
    @transaction.atomic
    def generate_invoices_for_order(order, is_inter_state=False, place_of_supply="Tamil Nadu"):
        existing = list(InHouseGSTInvoice.objects.filter(order=order))
        if existing:
            return existing

        created = []
        superuser_user = CoreUser.objects.filter(is_superuser=True).order_by("id").first()
        first_item = order.items.select_related("catalogue__owner").first()
        seller_user = first_item.catalogue.owner if first_item and first_item.catalogue else superuser_user
        buyer_user = order.user

        seller_role = (get_user_current_role(seller_user) or "").lower() if seller_user else "superuser"
        invoice_type = "b2b_merchant_to_seller" if seller_role == "merchant" else "b2c_seller_to_buyer"

        total_taxable = Decimal("0.00")
        total_gst_calc = Decimal("0.00")
        for item in order.items.select_related("catalogue").all():
            gst_pct = Decimal(str(item.catalogue.gst_percentage)) if item.catalogue else Decimal("18.00")
            line_total = Decimal(str(item.subtotal))
            divisor = Decimal("1") + (gst_pct / Decimal("100"))
            taxable = (line_total / divisor).quantize(Decimal("0.01"))
            total_taxable += taxable
            total_gst_calc += (line_total - taxable)

        if is_inter_state:
            cgst, sgst, igst = Decimal("0.00"), Decimal("0.00"), total_gst_calc
        else:
            cgst = (total_gst_calc / Decimal("2")).quantize(Decimal("0.01"))
            sgst = total_gst_calc - cgst
            igst = Decimal("0.00")

        created.append(InHouseGSTInvoice.objects.create(
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
            invoice_type=invoice_type,
            order=order,
            seller=seller_user,
            buyer=buyer_user,
            seller_gstin=InHouseGSTInvoiceService._get_user_gstin(seller_user),
            buyer_gstin=InHouseGSTInvoiceService._get_user_gstin(buyer_user),
            place_of_supply=place_of_supply,
            taxable_amount=total_taxable,
            cgst_amount=cgst,
            sgst_amount=sgst,
            igst_amount=igst,
            total_gst=total_gst_calc,
            grand_total=order.total_amount,
        ))

        platform_comm = CommissionProfile.objects.filter(
            order_id=order.order_number,
            recipient_role="superuser",
        ).first()
        if platform_comm and platform_comm.commission_amount > 0:
            comm_taxable = Decimal(str(platform_comm.commission_amount))
            c_cgst, c_sgst, c_igst, c_gst = InHouseGSTInvoiceService._split_gst(
                comm_taxable, Decimal("18.00"), is_inter_state=is_inter_state
            )
            created.append(InHouseGSTInvoice.objects.create(
                invoice_number=f"COM-{uuid.uuid4().hex[:8].upper()}",
                invoice_type="platform_commission",
                order=order,
                seller=superuser_user,
                buyer=seller_user,
                seller_gstin=InHouseGSTInvoiceService._get_user_gstin(superuser_user),
                buyer_gstin=InHouseGSTInvoiceService._get_user_gstin(seller_user),
                place_of_supply=place_of_supply,
                taxable_amount=comm_taxable,
                cgst_amount=c_cgst,
                sgst_amount=c_sgst,
                igst_amount=c_igst,
                total_gst=c_gst,
                grand_total=comm_taxable + c_gst,
            ))

        return created