from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import render
from apps.catalogs.core_catalogs.models import CoreCatalog
from apps.catalogs.core_catalogs.serializers import CoreCatalogSerializer

class CoreCatalogCreateListView(generics.ListCreateAPIView):
    serializer_class = CoreCatalogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # லாகின் செய்த பயனர் தனது சொந்தப் பொருட்களை மட்டும் பார்க்க முடியும்
        user = self.request.user
        if user.is_superuser:
            return CoreCatalog.objects.all()
        return CoreCatalog.objects.filter(vendor=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # பிரவுசரில் திறக்கும்போது HTML பக்கத்தைக் காண்பிக்க:
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            serializer = self.get_serializer(queryset, many=True)
            return render(request, 'catalogs/product_list.html', {'products': serializer.data})
            
        return super().list(request, *args, **kwargs)