from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from apps.users.merchant.models import MerchantProfile
from apps.users.merchant.serializers import MerchantProfileSerializer

class MerchantProfileCreateOrUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = MerchantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = MerchantProfile.objects.get_or_create(user=self.request.user)
        return profile

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def merchant_dashboard(request):
    profile, created = MerchantProfile.objects.get_or_create(user=request.user)
    
    # பிரவுசரில் திறக்கும்போது HTML பக்கத்தைக் காண்பிக்க:
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        return render(request, 'merchant/dashboard.html', {'profile': profile})
        
    # API / Postman மூலம் அழைத்தால் JSON தரவு கிடைக்கும்:
    serializer = MerchantProfileSerializer(profile)
    return Response({
        "status": "success",
        "message": "Welcome to the Merchant Dashboard",
        "profile": serializer.data
    })