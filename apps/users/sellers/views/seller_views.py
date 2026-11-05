from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from apps.users.sellers.models import SellerProfile
from apps.users.sellers.serializers import SellerProfileSerializer

class SellerProfileCreateOrUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = SellerProfile.objects.get_or_create(user=self.request.user)
        return profile

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def seller_dashboard(request):
    """
    Seller Dashboard View: HTML பக்கம் அல்லது JSON ரெஸ்பான்ஸ் வழங்கும்
    """
    profile, created = SellerProfile.objects.get_or_create(user=request.user)
    
    # பிரவுசரில் திறக்கும்போது HTML பக்கத்தைக் காண்பிக்க:
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        return render(request, 'sellers/dashboard.html', {'profile': profile})
        
    # API / Postman மூலம் அழைத்தால் JSON தரவு கிடைக்கும்:
    serializer = SellerProfileSerializer(profile)
    return Response({
        "status": "success",
        "message": "Welcome to the Seller Dashboard",
        "profile": serializer.data
    })