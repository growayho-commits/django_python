from rest_framework import viewsets, permissions
from apps.professional_network.models import ProfessionalProfile, ServiceRequest
from apps.professional_network.serializers.professional_serializer import (
    ProfessionalProfileSerializer, 
    ServiceRequestSerializer
)

class ProfessionalProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalProfile.objects.all()
    serializer_class = ProfessionalProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ServiceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ServiceRequest.objects.all()
        return ServiceRequest.objects.filter(
            client=user
        ) | ServiceRequest.objects.filter(professional__user=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)