from django.http import HttpResponseForbidden
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.users.executives.models import ExecutiveProfile
from apps.users.executives.serializers import ExecutiveProfileSerializer


class ExecutiveProfileCreateOrUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ExecutiveProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = ExecutiveProfile.objects.get_or_create(user=self.request.user)
        return profile


def _executive_can_access(profile, required_activity):
    if not required_activity:
        return True
    return profile.has_activity(required_activity)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def executive_dashboard(request, required_activity=None):
    profile, _ = ExecutiveProfile.objects.get_or_create(user=request.user)

    if not _executive_can_access(profile, required_activity):
        return HttpResponseForbidden('Access denied for this executive activity.')

    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
        return render(request, 'executives/dashboard.html', {
            'profile': profile,
            'activities': profile.assigned_activities or [],
        })

    serializer = ExecutiveProfileSerializer(profile)
    return Response({
        'status': 'success',
        'message': 'Welcome to the Executive Dashboard',
        'assigned_activities': profile.assigned_activities or [],
        'profile': serializer.data,
    })