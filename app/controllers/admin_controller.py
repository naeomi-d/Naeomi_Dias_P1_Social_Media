from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app.services.admin_service import AdminService
from app.utils.auth_utils import browser_role_required


admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route(
    "/admin/dashboard",
    methods=["GET"]
)
@browser_role_required("ADMIN")
def dashboard():

    users_page = request.args.get(
        "users_page",
        1,
        type=int
    )

    audit_page = request.args.get(
        "audit_page",
        1,
        type=int
    )

    users_page = max(users_page, 1)
    audit_page = max(audit_page, 1)

    per_page = 20

    users = AdminService.get_paginated_users(
        page=users_page,
        per_page=per_page
    )

    audit_logs = AdminService.get_paginated_audit_logs(
        page=audit_page,
        per_page=per_page
    )

    pending_reports = AdminService.get_pending_reports()

    total_users = AdminService.get_user_count()
    active_users = AdminService.get_active_user_count()
    inactive_users = AdminService.get_inactive_user_count()
    moderator_count = AdminService.get_moderator_count()

    total_audit_logs = AdminService.get_audit_log_count()

    return render_template(
        "admin_dashboard.html",

        users=users,
        audit_logs=audit_logs,
        pending_reports=pending_reports,

        total_users=total_users,
        active_users=active_users,
        inactive_users=inactive_users,
        moderator_count=moderator_count,
        total_audit_logs=total_audit_logs,

        users_page=users_page,
        audit_page=audit_page
    )

@admin_bp.route(
    "/admin/users/<int:user_id>/deactivate",
    methods=["POST"]
)
@browser_role_required("ADMIN")
def deactivate_user(user_id):

    try:

        AdminService.deactivate_user(
            user_id,
            session["user_id"]
        )

        flash(
            "User account has been deactivated.",
            "success"
        )

    except (ValueError, PermissionError) as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("admin.dashboard")
    )


@admin_bp.route(
    "/admin/users/<int:user_id>/activate",
    methods=["POST"]
)
@browser_role_required("ADMIN")
def activate_user(user_id):

    try:

        AdminService.activate_user(
            user_id,
            session["user_id"]
        )

        flash(
            "User account has been activated.",
            "success"
        )

    except (ValueError, PermissionError) as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("admin.dashboard")
    )


@admin_bp.route(
    "/admin/users/<int:user_id>/role",
    methods=["POST"]
)
@browser_role_required("ADMIN")
def change_user_role(user_id):

    new_role = request.form.get("role")

    try:

        AdminService.change_user_role(
            user_id,
            session["user_id"],
            new_role
        )

        flash(
            f"User role changed to {new_role}.",
            "success"
        )

    except (ValueError, PermissionError) as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("admin.dashboard")
    )


@admin_bp.route(
    "/admin/reports/<int:report_id>/review",
    methods=["POST"]
)
@browser_role_required("ADMIN")
def review_report(report_id):

    status = request.form.get("status")

    try:

        AdminService.review_report(
            report_id,
            session["user_id"],
            status
        )

        flash(
            f"Report #{report_id} marked as {status}.",
            "success"
        )

    except (ValueError, PermissionError) as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("admin.dashboard")
    )