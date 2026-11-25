from django.http import JsonResponse
from apps.common.choices import CoverageScopeChoices


def coverage_scopes_api(request):
    """Return standardized coverage scope choices for forms and frontend filters."""
    return JsonResponse({
        "status": "success",
        "scopes": [
            {"value": value, "label": label}
            for value, label in CoverageScopeChoices.choices
        ],
    })