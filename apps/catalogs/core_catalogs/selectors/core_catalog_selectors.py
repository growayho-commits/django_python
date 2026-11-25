from django.db.models import Q
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.catalogs.core_catalogs.services.delivery_coverage_service import CatalogueDeliveryCoverageService


class CoreCatalogSelector:
    """Centralized read queries for CoreCatalogProfile across all user roles."""

    @staticmethod
    def _base_queryset():
        return CoreCatalogProfile.objects.select_related(
            "owner", "category", "commission_pricing", "inventory"
        ).prefetch_related(
            "pricing_tiers", "variants", "medias", "specifications"
        )

    @classmethod
    def get_all_catalogues(cls):
        return cls._base_queryset().all()

    @classmethod
    def get_owner_catalogues(cls, user):
        return cls._base_queryset().filter(owner=user)

    @classmethod
    def get_approved_marketplace_catalogues(
        cls,
        category_id=None,
        search_query="",
        pincode=None,
        taluk=None,
        district=None,
        state=None,
    ):
        qs = cls._base_queryset().filter(is_active=True, approval_status="approved")
        if category_id:
            qs = qs.filter(category_id=category_id)
        if search_query:
            qs = qs.filter(
                Q(name__icontains=search_query)
                | Q(brand_name__icontains=search_query)
                | Q(sku__icontains=search_query)
                | Q(description__icontains=search_query)
            )
        return CatalogueDeliveryCoverageService.filter_deliverable_catalogues(
            qs, pincode=pincode, taluk=taluk, district=district, state=state
        )

from django.db.models import Q
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.catalogs.core_catalogs.services.delivery_coverage_service import CatalogueDeliveryCoverageService


class CoreCatalogSelector:
    """Centralized read queries for CoreCatalogProfile across all user roles."""

    @staticmethod
    def _base_queryset():
        return CoreCatalogProfile.objects.select_related(
            "owner", "category", "commission_pricing", "inventory"
        ).prefetch_related(
            "pricing_tiers", "variants", "medias", "specifications"
        )

    @classmethod
    def get_all_catalogues(cls):
        return cls._base_queryset().all()

    @classmethod
    def get_owner_catalogues(cls, user):
        return cls._base_queryset().filter(owner=user)

    @classmethod
    def get_approved_marketplace_catalogues(
        cls,
        category_id=None,
        search_query="",
        trade_channel=None,
        pincode=None,
        taluk=None,
        district=None,
        state=None,
    ):
        qs = cls._base_queryset().filter(is_active=True, approval_status="approved")
        if trade_channel in {"b2b", "b2c"}:
            qs = qs.filter(Q(trade_channel=trade_channel) | Q(trade_channel="both"))
        if category_id:
            qs = qs.filter(category_id=category_id)
        if search_query:
            qs = qs.filter(
                Q(name__icontains=search_query)
                | Q(brand_name__icontains=search_query)
                | Q(sku__icontains=search_query)
                | Q(description__icontains=search_query)
            )
        return CatalogueDeliveryCoverageService.filter_deliverable_catalogues(
            qs, pincode=pincode, taluk=taluk, district=district, state=state
        )