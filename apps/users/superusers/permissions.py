from functools import wraps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


def superuser_required(view_func):
    """Allow access only to authenticated superusers."""
    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden('Access denied. Superusers only.')
        return view_func(request, *args, **kwargs)
    return _wrapped


def role_required(*allowed_roles):
    """
    Allow access only to users whose active role is in allowed_roles (or superusers).
    """
    normalized = {r.lower() for r in allowed_roles}

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            current_role = get_user_current_role(request.user).lower()
            if current_role not in normalized:
                return HttpResponseForbidden(
                    f'Access denied. Required role: {", ".join(sorted(normalized))}.'
                )
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def executive_activity_required(*required_activities):
    """
    Allow access to executives only if at least one required activity is in
    ExecutiveProfile.assigned_activities (superusers always allowed).
    """
    required_set = {a.lower() for a in required_activities}

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if get_user_current_role(request.user).lower() != 'executive':
                return HttpResponseForbidden('Access denied. Executives only.')

            exec_profile = ExecutiveProfile.objects.filter(user=request.user).first()
            assigned = {
                a.lower() for a in (exec_profile.assigned_activities or [])
            } if exec_profile else set()

            if required_set and not (assigned & required_set):
                return HttpResponseForbidden(
                    f'Access denied. Missing executive activity: {", ".join(sorted(required_set))}.'
                )
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator