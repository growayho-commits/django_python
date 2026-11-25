class LocationCoverageService:
    """Shared geographic & online coverage matcher for Catalogs, Professional Network, and Logistics."""

    @staticmethod
    def _normalized_set(locations) -> set[str]:
        if not locations:
            return set()
        return {str(loc).strip().lower() for loc in locations if str(loc).strip()}

    @classmethod
    def is_covered(
        cls,
        scope: str,
        locations,
        pincode=None,
        taluk=None,
        district=None,
        state=None,
        include_online: bool = False,
    ) -> bool:
        scope_val = (scope or "all_india").lower()
        if scope_val == "all_india":
            return True
        if scope_val == "online":
            return include_online

        covered = cls._normalized_set(locations)
        if not covered:
            return False

        if scope_val == "pincode":
            return bool(pincode and str(pincode).strip().lower() in covered)
        if scope_val == "taluk":
            return bool(taluk and str(taluk).strip().lower() in covered)
        if scope_val in ("district", "multi_district"):
            return bool(district and str(district).strip().lower() in covered)
        if scope_val in ("state", "multi_state"):
            return bool(state and str(state).strip().lower() in covered)

        return False

    @classmethod
    def filter_queryset_by_location(
        cls,
        queryset,
        scope_field: str = "delivery_scope",
        locations_field: str = "delivery_locations",
        pincode=None,
        taluk=None,
        district=None,
        state=None,
        include_online: bool = False,
    ):
        if not any([pincode, taluk, district, state]):
            return queryset

        matching_ids = [
            obj.id
            for obj in queryset
            if cls.is_covered(
                getattr(obj, scope_field, "all_india"),
                getattr(obj, locations_field, []),
                pincode=pincode,
                taluk=taluk,
                district=district,
                state=state,
                include_online=include_online,
            )
        ]
        return queryset.filter(id__in=matching_ids)