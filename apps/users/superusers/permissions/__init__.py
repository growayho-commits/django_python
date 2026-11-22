from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from apps.users.superusers.services.role_request_service import get_user_current_role


def superuser_required(view_func):
    """Allow access only to authenticated superusers or staff users."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Access denied. Superuser privileges are required.')
            return redirect('users:role_dashboard_redirect')
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def role_required(*allowed_roles):
    """Allow access only to users whose active role matches allowed_roles (or superuser)."""
    normalized_roles = {role.lower() for role in allowed_roles}

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users:login')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            current_role = (get_user_current_role(request.user) or '').lower()
            if current_role not in normalized_roles:
                messages.error(request, 'Access denied for your current role.')
                return redirect('users:role_dashboard_redirect')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def executive_activity_required(*required_activities):
    """Allow access to superusers or executives assigned to any of the required departments."""
    required_set = set(required_activities)

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users:login')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            current_role = (get_user_current_role(request.user) or '').lower()
            if current_role != 'executive':
                messages.error(request, 'Executive access is required.')
                return redirect('users:role_dashboard_redirect')

            exec_profile = getattr(request.user, 'executive_profile', None)
            assigned = set(getattr(exec_profile, 'assigned_activities', []) or [])
            if required_set and not assigned.intersection(required_set):
                messages.error(request, 'You do not have permission for this department activity.')
                return redirect('users:role_dashboard_redirect')
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator