from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    session,
    request
)

from app.services.report_service import ReportService
from app.utils.auth_utils import login_required


report_bp = Blueprint(
    "report",
    __name__
)


@report_bp.route(
    "/posts/<int:post_id>/report",
    methods=["POST"]
)
@login_required
def report_post(post_id):

    reason = request.form.get("reason")
    description = request.form.get("description")

    try:

        ReportService.report_post(
            session["user_id"],
            post_id,
            reason,
            description
        )

        flash(
            "Post reported successfully.",
            "success"
        )

    except ValueError as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("home.home")
    )
@report_bp.route(
    "/users/<int:user_id>/report",
    methods=["POST"]
)
@login_required
def report_user(user_id):

    reason = request.form.get("reason")
    description = request.form.get("description")

    try:

        ReportService.report_user(
            session["user_id"],
            user_id,
            reason,
            description
        )

        flash(
            "User reported successfully.",
            "success"
        )

    except ValueError as error:

        flash(
            str(error),
            "danger"
        )

    return redirect(
        url_for("home.home")
    )