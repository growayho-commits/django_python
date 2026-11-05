from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render
from apps.users.superusers.models import SuperuserProfile
from apps.users.superusers.serializers import SuperuserProfileSerializer

class SuperuserProfileCreateOrUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SuperuserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = SuperuserProfile.objects.get_or_create(user=self.request.user)
        return profile

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def superuser_dashboard(request):
    """
    Superuser Dashboard View: HTML பக்கம் அல்லது JSON ரெஸ்பான்ஸ் வழங்கும்
    """
    profile, created = SuperuserProfile.objects.get_or_create(user=request.user)
    
    # பிரவுசரில் திறக்கும்போது HTML பக்கத்தைக் காண்பிக்க:
    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        return render(request, 'superusers/dashboard.html', {'profile': profile})
        
    # API / Postman மூலம் அழைத்தால் JSON தரவு கிடைக்கும்:
    serializer = SuperuserProfileSerializer(profile)
    return Response({
        "status": "success",
        "message": "Welcome to the Superuser Dashboard",
        "profile": serializer.data
    })