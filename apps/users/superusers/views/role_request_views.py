from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

import json
from apps.users.superusers.models import RoleUpgradeRequest
from apps.users.superusers.models.role_upgrade_request import SUB_ROLE_OPTIONS
from apps.users.superusers.forms.role_forms import RoleUpgradeRequestForm
from apps.users.superusers.serializers.role_request_serializer import RoleUpgradeRequestSerializer
from apps.users.superusers.services.role_request_service import (
    RoleUpgradeRequestService,
    get_user_current_role,
)
from apps.users.superusers.views.superuser_views import get_user_dashboard_url


@login_required
def submit_role_request_view(request):
    """
    Allows Members, Sellers, Merchants, and Executives to submit a new role
    upgrade request and view their request history.
    """
    if request.user.is_superuser:
        return redirect("users:manage_roles")

    user = request.user
    my_requests = RoleUpgradeRequest.objects.filter(user=user).order_by("-created_at")

    pending_role_names = list(
        my_requests.filter(status="pending").values_list("requested_role", flat=True)
    )
    current_role = get_user_current_role(user)
    excluded_roles = set(pending_role_names + [current_role])

    if request.method == "POST":
        form = RoleUpgradeRequestForm(request.POST)
        if form.is_valid():
            role_req = form.save(commit=False)
            role_req.sub_roles = request.POST.getlist('sub_roles')
            if role_req.requested_role in excluded_roles:
                messages.error(
                    request,
                    "You already have a pending request or already hold this role.",
                )
            else:
                role_req.user = user
                role_req.status = "pending"
                role_req.save()
                messages.success(
                    request,
                    "Your upgrade request has been submitted successfully!",
                )
                return redirect("users:submit_role_request")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RoleUpgradeRequestForm()

    if "requested_role" in form.fields:
        current_choices = form.fields["requested_role"].choices
        form.fields["requested_role"].choices = [
            (val, label)
            for val, label in current_choices
            if val.lower() not in [r.lower() for r in excluded_roles]
        ]

    dashboard_url = get_user_dashboard_url(user)

    context = {
        "form": form,
        "my_requests": my_requests,
        "current_role": current_role,
        "dashboard_url": dashboard_url,
    }
    context["sub_role_options_json"] = json.dumps(SUB_ROLE_OPTIONS)
    return render(request, "members/submit_role_request.html", context)


@login_required
def manage_roles_view(request):
    """
    Superuser view to list and manage all role upgrade requests across
    Member, Seller, Merchant, and Executive roles.
    """
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Superusers only.")
        return redirect("/")

    current_status = request.GET.get("status", "pending")
    role_filter = request.GET.get("role", "all")

    if request.method == "POST":
        req_id = request.POST.get("request_id")
        action = request.POST.get("action")
        remarks = request.POST.get("admin_remarks", "")

        if req_id and action in ["approve", "reject", "reconsider"]:
            RoleUpgradeRequestService.update_status_and_notify(req_id, action, remarks)
            messages.success(request, f"Role request successfully {action}ed.")
            return redirect(f"{request.path}?status={current_status}&role={role_filter}")

    qs = RoleUpgradeRequest.objects.select_related("user").order_by("-created_at")
    if current_status != "all":
        qs = qs.filter(status=current_status)

    role_requests = []
    for req in qs:
        current_role = get_user_current_role(req.user)
        req.current_role_display = current_role
        if role_filter == "all" or current_role == role_filter:
            role_requests.append(req)

    context = {
        "role_requests": role_requests,
        "current_status": current_status,
        "role_filter": role_filter,
    }
    return render(request, "superusers/manage_role_requests.html", context)


@login_required
def handle_role_request(request, pk):
    if not request.user.is_superuser:
        return redirect("/")
    role_req = get_object_or_404(RoleUpgradeRequest, pk=pk)
    if request.method == "POST":
        action = request.POST.get("action")
        remarks = request.POST.get("admin_remarks", "")
        if action in ["approve", "reject", "reconsider"]:
            RoleUpgradeRequestService.update_status_and_notify(role_req.id, action, remarks)
            messages.success(request, f"Role request marked as {action}.")
        return redirect("users:manage_roles")
    return render(request, "superusers/role_request_action.html", {"role_req": role_req})


@login_required
def assign_role_view(request):
    if not request.user.is_superuser:
        return redirect("/")
    messages.info(request, "Direct assignment is handled via RoleUpgradeRequest now.")
    return redirect("users:manage_roles")


@login_required
def toggle_role_status_view(request, assignment_id):
    if not request.user.is_superuser:
        return redirect("/")
    messages.info(request, "Role status management updated.")
    return redirect("users:manage_roles")


@login_required
def update_role_requirement(request):
    if not request.user.is_superuser:
        return redirect("/")
    return render(request, "superusers/update_requirement.html")


class UserRoleUpgradeRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_requests = RoleUpgradeRequest.objects.filter(user=request.user).order_by("-created_at")
        serializer = RoleUpgradeRequestSerializer(user_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoleUpgradeRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, status="pending")
            return Response(
                {"message": "Role request submitted successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuperuserRoleUpgradeRequestManageView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        status_filter = request.GET.get("status", "pending")
        requests_qs = RoleUpgradeRequest.objects.filter(status=status_filter).order_by("-created_at")
        serializer = RoleUpgradeRequestSerializer(requests_qs, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        action = request.data.get("action")
        remarks = request.data.get("admin_remarks", "")
        try:
            updated_req = RoleUpgradeRequestService.update_status_and_notify(pk, action, remarks)
            return Response(
                {"message": f"Successfully {action}ed request.", "status": updated_req.status},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
role_request_view = submit_role_request_view

