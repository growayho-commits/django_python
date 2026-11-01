from ..models.tax_profile import TaxProfile

class TaxService:
    @staticmethod
    def calculate_tax(amount, tax_name):
        try:
            tax = TaxProfile.objects.get(tax_name=tax_name, is_active=True)
            tax_amount = (amount * tax.percentage) / 100
            return tax_amount
        except TaxProfile.DoesNotExist:
            return 0.0