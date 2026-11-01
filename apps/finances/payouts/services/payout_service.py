from ..models.payout_profile import PayoutProfile

class PayoutService:
    @staticmethod
    def initiate_payout(vendor, amount):
        return PayoutProfile.objects.create(vendor=vendor, amount=amount, status='processing')

    @staticmethod
    def complete_payout(payout_id, txn_ref):
        payout = PayoutProfile.objects.get(id=payout_id)
        payout.status = 'completed'
        payout.transaction_reference = txn_ref
        payout.save()
        return payout