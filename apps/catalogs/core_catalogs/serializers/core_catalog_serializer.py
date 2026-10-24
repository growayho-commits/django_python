from rest_framework import serializers
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CoreCatalogSerializer(serializers.ModelSerializer):
    """
    REST API Data Formatter for Core Catalog[cite: 1, 2].
    """
    class Meta:
        model = CoreCatalog
        fields = [
            'id', 'catalog_code', 'title', 'slug', 'catalog_type',
            'brand_name', 'root_category', 'sub_category',
            'short_description', 'long_description',
            'hsn_or_sac_code', 'gst_percentage',
            'is_active', 'is_draft', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'catalog_type', 'created_at', 'updated_at']
```[cite: 1, 2]

---

### 2. Views Layer (`apps/catalogs/core_catalogs/views/core_catalog_views.py`)
HTTP கோரிக்கைகளைப் பெற்று, Selectors (படிக்க) மற்றும் Application Services (எழுத) மூலமாகக் கோரிக்கையைக் கையாளும் கட்டுப்பாட்டு அடுக்கு (Controller)[cite: 1, 2]:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.core_catalogs.serializers.core_catalog_serializer import CoreCatalogSerializer
from apps.catalogs.core_catalogs.dtos.core_catalog_dtos import CoreCatalogCreateDTO
from apps.catalogs.core_catalogs.services.core_catalog_service import CoreCatalogApplicationService

class CoreCatalogCreateAPIView(APIView):
    """
    API Controller for registering a new Catalog enforcing SoC and DDD[cite: 1, 2].
    """
    def post(self, request):
        serializer = CoreCatalogSerializer(data=request.data)
        if serializer.is_valid():
            # Pass validated data to DTO for type-safe domain handling
            dto = CoreCatalogCreateDTO(**serializer.validated_data)
            
            try:
                catalog = CoreCatalogApplicationService.register_new_catalog(dto)
                response_serializer = CoreCatalogSerializer(catalog)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```[cite: 1, 2]

---

இந்த முறையில் Views நேரடியாக டேட்டாபேஸுடன் பேசாமல், **DTOs மற்றும் Application Services** வழியாகவே அனைத்து எழுதுதல் (Write) செயல்பாடுகளையும் செய்கின்றன[cite: 1, 2]. இதுவே உண்மையான Clean Architecture மற்றும் SoC முறையாகும்[cite: 1, 2]. 

இதன் தொடர்ச்சியாக மற்ற சப்-ஆப்களுக்கான Views மற்றும் URLs இணைப்புகளை உருவாக்கலாமா?