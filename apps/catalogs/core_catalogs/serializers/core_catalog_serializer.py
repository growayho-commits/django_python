from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.catalogs.core_catalogs.validators.core_catalog_validators import validate_unique_catalogue_name


class CoreCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreCatalogProfile
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def validate_name(self, value):
        try:
            return validate_unique_catalogue_name(value, instance=self.instance)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages)