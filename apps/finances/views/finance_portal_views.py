from decimal import Decimal
import uuid

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.finances.bank_accounts.models.bank_account_profile import BankAccountProfile
from apps.finances.commissions.models.commission_profile import CommissionProfile
from apps.finances.payment_gateways.models.gateway_profile import EscrowTransaction
from apps.finances.payment_gateways.services.escrow_service import EscrowPaymentService
from apps.finances.payouts.models.payout_profile import LoyaltyWallet, PayoutProfile, WalletTransaction
from apps.finances.taxes.models.tax_profile import InHouseGSTInvoice
from apps.finances.taxes.services.gst_invoice_service import InHouseGSTInvoiceService
from apps.marketing_leads.orders.models.order_profile import OrderProfile

CoreUser = get_user_model()


@login_required
def escrow_dashboard_view(request):
    is_admin = request.user.is_superuser

    if request.method == "POST" and is_admin:
        action = request.POST.get("action")
        order_id = request.POST.get("order_id")
        if action == "hold_escrow" and order_id:
            EscrowPaymentService.hold_payment_in_escrow(order_id)
            messages.success(request, "Payment held in Escrow.")
        elif action == "release_escrow" and order_id:
            result = EscrowPaymentService.release_escrow_to_seller(order_id)
            messages.success(request, f"Escrow released & {len(result['splits'])} commission record(s) generated.")
        return redirect("finances:escrow_dashboard")

    if is_admin:
        orders = OrderProfile.objects.select_related("user").order_by("-created_at")[:50]
        escrows = EscrowTransaction.objects.select_related("order", "buyer").order_by("-held_at")[:50]
    else:
        orders = OrderProfile.objects.filter(user=request.user).order_by("-created_at")[:30]
        escrows = EscrowTransaction.objects.filter(buyer=request.user).select_related("order").order_by("-held_at")[:30]

    return render(request, "finances/escrow_dashboard.html", {
        "is_admin": is_admin,
        "orders": orders,
        "escrows": escrows,
    })


@login_required
def bank_accounts_portal_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_bank":
            holder = request.POST.get("account_holder_name", "").strip()
            number = request.POST.get("account_number", "").strip()
            ifsc = request.POST.get("ifsc_code", "").strip().upper()
            bank_name = request.POST.get("bank_name", "").strip()
            is_primary = bool(request.POST.get("is_primary"))
            if holder and number and ifsc and bank_name:
                if is_primary:
                    BankAccountProfile.objects.filter(user=request.user).update(is_primary=False)
                try:
                    BankAccountProfile.objects.create(
                        user=request.user,
                        account_holder_name=holder,
                        account_number=number,
                        ifsc_code=ifsc,
                        bank_name=bank_name,
                        is_primary=is_primary,
                    )
                    messages.success(request, "Bank account added successfully.")
                except IntegrityError:
                    messages.error(request, "This account number is already registered.")

        elif action == "set_primary":
            acc = get_object_or_404(BankAccountProfile, pk=request.POST.get("account_id"), user=request.user)
            BankAccountProfile.objects.filter(user=request.user).update(is_primary=False)
            acc.is_primary = True
            acc.save(update_fields=["is_primary"])
            messages.success(request, f"{acc.bank_name} set as primary.")

        elif action == "delete_bank":
            BankAccountProfile.objects.filter(pk=request.POST.get("account_id"), user=request.user).delete()
            messages.info(request, "Bank account removed.")

        return redirect("finances:bank_portal")

    accounts = BankAccountProfile.objects.filter(user=request.user).order_by("-is_primary", "-created_at")
    return render(request, "finances/bank_accounts.html", {"accounts": accounts})


@login_required
def payouts_portal_view(request):
    is_admin = request.user.is_superuser

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "request_payout":
            try:
                amount = float(request.POST.get("amount") or 0)
            except ValueError:
                amount = 0
            if amount > 0:
                PayoutProfile.objects.create(
                    vendor=request.user,
                    amount=amount,
                    status="processing",
                    transaction_reference=f"PAY-{uuid.uuid4().hex[:8].upper()}",
                )
                messages.success(request, f"Payout request for INR {amount:.2f} submitted.")

        elif action == "mark_paid" and is_admin:
            payout = get_object_or_404(PayoutProfile, pk=request.POST.get("payout_id"))
            payout.status = "paid"
            payout.processed_at = timezone.now()
            payout.save(update_fields=["status", "processed_at"])
            messages.success(request, f"Payout #{payout.id} marked as Paid.")

        return redirect("finances:payout_portal")

    if is_admin:
        commissions = CommissionProfile.objects.select_related("vendor").order_by("-created_at")[:50]
        payouts = PayoutProfile.objects.select_related("vendor").order_by("-created_at")[:50]
    else:
        commissions = CommissionProfile.objects.filter(vendor=request.user).order_by("-created_at")[:50]
        payouts = PayoutProfile.objects.filter(vendor=request.user).order_by("-created_at")[:50]

    total_earned = CommissionProfile.objects.filter(vendor=request.user).aggregate(s=Sum("commission_amount"))["s"] or 0

    return render(request, "finances/payouts_portal.html", {
        "is_admin": is_admin,
        "commissions": commissions,
        "payouts": payouts,
        "total_earned": total_earned,
    })


@login_required
def loyalty_wallet_view(request):
    wallet, _ = LoyaltyWallet.objects.get_or_create(user=request.user)
    is_admin = request.user.is_superuser

    if request.method == "POST" and is_admin:
        target_email = request.POST.get("target_email", "").strip()
        points = Decimal(str(request.POST.get("points") or 0))
        note = request.POST.get("note", "Referral / Loyalty Reward").strip()
        target_user = CoreUser.objects.filter(email__iexact=target_email).first()
        if target_user and points > 0:
            target_wallet, _ = LoyaltyWallet.objects.get_or_create(user=target_user)
            target_wallet.loyalty_points += points
            target_wallet.save(update_fields=["loyalty_points"])
            WalletTransaction.objects.create(
                wallet=target_wallet,
                tx_type="credit",
                points_delta=points,
                reference_note=note,
            )
            messages.success(request, f"Credited {points} loyalty points to {target_user.email}.")
        else:
            messages.error(request, "Valid user email and positive points required.")
        return redirect("finances:loyalty_wallet")

    transactions = wallet.transactions.order_by("-created_at")[:50]
    return render(request, "finances/loyalty_wallet.html", {
        "wallet": wallet,
        "transactions": transactions,
        "is_admin": is_admin,
    })


@login_required
def gst_invoices_view(request):
    is_admin = request.user.is_superuser

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        is_inter_state = bool(request.POST.get("is_inter_state"))
        place_of_supply = request.POST.get("place_of_supply", "Tamil Nadu").strip() or "Tamil Nadu"
        order = get_object_or_404(OrderProfile, pk=order_id)
        if is_admin or order.user_id == request.user.id or order.items.filter(catalogue__owner=request.user).exists():
            invoices = InHouseGSTInvoiceService.generate_invoices_for_order(
                order=order,
                is_inter_state=is_inter_state,
                place_of_supply=place_of_supply,
            )
            messages.success(request, f"{len(invoices)} GST Tax Invoice(s) ready for {order.order_number}.")
        return redirect("finances:gst_invoices")

    if is_admin:
        invoices = InHouseGSTInvoice.objects.select_related("order", "seller", "buyer").order_by("-issued_at")[:50]
        orders = OrderProfile.objects.order_by("-created_at")[:30]
    else:
        invoices = InHouseGSTInvoice.objects.filter(
            Q(buyer=request.user) | Q(seller=request.user)
        ).select_related("order", "seller", "buyer").order_by("-issued_at")[:50]
        orders = OrderProfile.objects.filter(
            Q(user=request.user) | Q(items__catalogue__owner=request.user)
        ).distinct().order_by("-created_at")[:30]

    return render(request, "finances/gst_invoices.html", {
        "invoices": invoices,
        "orders": orders,
    })


@login_required
def gst_invoice_print_view(request, pk):
    invoice = get_object_or_404(InHouseGSTInvoice.objects.select_related("order", "seller", "buyer"), pk=pk)
    return render(request, "finances/gst_invoice_print.html", {"invoice": invoice})