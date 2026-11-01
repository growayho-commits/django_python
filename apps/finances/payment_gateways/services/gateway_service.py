from ..models.gateway_profile import PaymentGatewayConfig

class PaymentGatewayService:
    @staticmethod
    def get_active_gateways():
        return PaymentGatewayConfig.objects.filter(is_active=True)

    @staticmethod
    def update_gateway_status(gateway_id, is_active):
        try:
            gateway = PaymentGatewayConfig.objects.get(id=gateway_id)
            gateway.is_active = is_active
            gateway.save()
            return gateway
        except PaymentGatewayConfig.DoesNotExist:
            raise ValueError("Payment gateway configuration not found.")