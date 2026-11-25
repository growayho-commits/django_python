class CatalogueDeliveryCoverageService:
    """Checks and filters catalogues based on buyer delivery location."""

    @staticmethod
    def _normalized_set(locations) -> set[str]:
        if not locations:
            return set()
        return {str(loc).strip().lower() for loc in locations if str(loc).strip()}

    @classmethod
    def is_deliverable_to(cls, catalogue, pincode=None, taluk=None, district=None, state=None) -> bool:
        scope = getattr(catalogue, "delivery_scope", "all_india")
        if scope == "all_india":
            return True

        covered = cls._normalized_set(getattr(catalogue, "delivery_locations", []))
        if not covered:
            return False

        if scope == "pincode":
            return bool(pincode and str(pincode).strip().lower() in covered)
        if scope == "taluk":
            return bool(taluk and str(taluk).strip().lower() in covered)
        if scope in ("district", "multi_district"):
            return bool(district and str(district).strip().lower() in covered)
        if scope in ("state", "multi_state"):
            return bool(state and str(state).strip().lower() in covered)

        return False

    @classmethod
    def filter_deliverable_catalogues(cls, queryset, pincode=None, taluk=None, district=None, state=None):
        """Return only catalogues deliverable to the given address details."""
        if not any([pincode, taluk, district, state]):
            return queryset

        matching_ids = [
            cat.id
            for cat in queryset
            if cls.is_deliverable_to(cat, pincode=pincode, taluk=taluk, district=district, state=state)
        ]
        return queryset.filter(id__in=matching_ids)