from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)

from app.services.moderator_service import ModeratorService
from app.utils.auth_utils import browser_role_required


moderator_bp = Blueprint(
    "moderator",
    __name__
)



@moderator_bp.route(
    "/moderator/dashboard",
    methods=["GET"]
)
@browser_role_required("MODERATOR", "ADMIN")
def dashboard():

    reports = ModeratorService.get_pending_reports()

    return render_template(
        "moderator_dashboard.html",
        reports=reports
    )



@moderator_bp.route(
    "/moderator/reports/<int:report_id>/dismiss",
    methods=["POST"]
)
@browser_role_required("MODERATOR", "ADMIN")
def dismiss_report(report_id):

    try:

        ModeratorService.dismiss_report(
            report_id,
            session["user_id"]
        )

        flash(
            f"Report #{report_id} has been dismissed.",
            "success"
        )

    except (ValueError, PermissionError) as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("moderator.dashboard")
    )


@moderator_bp.route(
    "/moderator/reports/<int:report_id>/review",
    methods=["POST"]
)
@browser_role_required("MODERATOR", "ADMIN")
def review_report(report_id):

    try:

        status = request.form.get("status")

        ModeratorService.review_report(
            report_id,
            session["user_id"],
            status
        )

        flash(
            f"Report #{report_id} has been reviewed.",
            "success"
        )

    except (ValueError, PermissionError) as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("moderator.dashboard")
    )

@moderator_bp.route(
    "/moderator/reports/<int:report_id>/remove-post",
    methods=["POST"]
)
@browser_role_required("MODERATOR", "ADMIN")
def remove_reported_post(report_id):

    try:

        ModeratorService.remove_reported_post(
            report_id,
            session["user_id"]
        )

        flash(
            "Reported post has been removed.",
            "success"
        )

    except (ValueError, PermissionError) as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("moderator.dashboard")
    )

@moderator_bp.route(
    "/moderator/reports/<int:report_id>/deactivate-user",
    methods=["POST"]
)
@browser_role_required("MODERATOR", "ADMIN")
def deactivate_reported_user(report_id):

    try:

        ModeratorService.deactivate_reported_user(
            report_id,
            session["user_id"]
        )

        flash(
            "Reported user has been deactivated.",
            "success"
        )

    except (ValueError, PermissionError) as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("moderator.dashboard")
    )

@moderator_bp.route(
    "/moderator/reports/<int:report_id>",
    methods=["GET"]
)
@browser_role_required("MODERATOR", "ADMIN")
def report_detail(report_id):

    try:

        report, post, user = ModeratorService.get_report_for_review(
            report_id
        )

        return render_template(
            "moderator_report_detail.html",
            report=report,
            post=post,
            user=user
        )

    except (ValueError, PermissionError) as error:

        flash(
            str(error),
            "danger"
        )

        return redirect(
            url_for("moderator.dashboard")
        )