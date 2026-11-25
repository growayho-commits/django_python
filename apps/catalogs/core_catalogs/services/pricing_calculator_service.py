from decimal import Decimal, ROUND_HALF_UP


def _round_money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _compute_commission(base_amount: Decimal, mode: str, value: Decimal, quantity: int) -> Decimal:
    if not value or value <= 0:
        return Decimal("0.00")
    if mode == "percentage":
        return _round_money((base_amount * value) / Decimal("100"))
    return _round_money(value * Decimal(quantity))


class CataloguePricingCalculatorService:
    """
    Calculates final catalogue pricing step-by-step:
    1. Base Price
    2. Bulk Quantity Tier
    3. Superuser, Executive, and Seller Commissions (% or Flat)
    4. Extra Handling, GST, and Transport Included / Extra Delivery Charge
    """

    @staticmethod
    def calculate_price_breakdown(catalogue, quantity: int = 1) -> dict:
        qty = max(1, int(quantity))
        base_unit_price = Decimal(catalogue.base_price or 0)
        effective_unit_price = base_unit_price
        applied_tier_name = None

        # Step 2: Match active bulk quantity tier
        tiers = catalogue.pricing_tiers.filter(is_active=True, min_quantity__lte=qty).order_by("-min_quantity")
        for tier in tiers:
            if tier.max_quantity is None or qty <= tier.max_quantity:
                applied_tier_name = tier.tier_name
                t_val = Decimal(tier.tier_value or 0)
                if tier.adjustment_type == "fixed_price":
                    effective_unit_price = t_val
                elif tier.adjustment_type == "percentage_off":
                    effective_unit_price = max(Decimal("0.00"), base_unit_price - ((base_unit_price * t_val) / Decimal("100")))
                elif tier.adjustment_type == "flat_off":
                    effective_unit_price = max(Decimal("0.00"), base_unit_price - t_val)
                break

        effective_unit_price = _round_money(effective_unit_price)
        base_subtotal = _round_money(effective_unit_price * Decimal(qty))

        # Step 3: Role Commissions & Extra Charges
        commission_cfg = getattr(catalogue, "commission_pricing", None)
        superuser_comm = Decimal("0.00")
        executive_comm = Decimal("0.00")
        seller_comm = Decimal("0.00")
        handling_charge = Decimal("0.00")
        delivery_extra_charge = Decimal("0.00")

        if commission_cfg and commission_cfg.is_active:
            superuser_comm = _compute_commission(
                base_subtotal, commission_cfg.superuser_commission_mode, Decimal(commission_cfg.superuser_commission_value or 0), qty
            )
            executive_comm = _compute_commission(
                base_subtotal, commission_cfg.executive_commission_mode, Decimal(commission_cfg.executive_commission_value or 0), qty
            )
            seller_comm = _compute_commission(
                base_subtotal, commission_cfg.seller_commission_mode, Decimal(commission_cfg.seller_commission_value or 0), qty
            )
            handling_charge = _round_money(Decimal(commission_cfg.extra_handling_charge or 0))
            if not catalogue.transport_included:
                delivery_extra_charge = _round_money(Decimal(commission_cfg.estimated_delivery_charge or 0))

        total_commission = _round_money(superuser_comm + executive_comm + seller_comm)
        taxable_amount = _round_money(base_subtotal + total_commission + handling_charge)

        # Step 4: GST & Transport
        gst_rate = Decimal(catalogue.gst_percentage or 0)
        gst_amount = _round_money((taxable_amount * gst_rate) / Decimal("100"))
        final_total = _round_money(taxable_amount + gst_amount + delivery_extra_charge)

        return {
            "catalogue_id": catalogue.id,
            "catalogue_name": catalogue.name,
            "quantity": qty,
            "base_unit_price": base_unit_price,
            "applied_tier_name": applied_tier_name,
            "effective_unit_price": effective_unit_price,
            "base_subtotal": base_subtotal,
            "superuser_commission": superuser_comm,
            "executive_commission": executive_comm,
            "seller_commission": seller_comm,
            "total_commission": total_commission,
            "extra_handling_charge": handling_charge,
            "taxable_amount": taxable_amount,
            "gst_percentage": gst_rate,
            "gst_amount": gst_amount,
            "transport_included": catalogue.transport_included,
            "delivery_charge_label": catalogue.delivery_charge_label,
            "delivery_extra_charge": delivery_extra_charge,
            "final_total": final_total,
        }