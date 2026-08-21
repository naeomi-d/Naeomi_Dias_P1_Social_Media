from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    session
)

from app.services.follow_service import FollowService
from app.utils.auth_utils import login_required


follow_bp = Blueprint(
    "follow",
    __name__
)


# ==================== JINJA FOLLOW ====================

@follow_bp.route(
    "/users/<int:user_id>/follow",
    methods=["POST"]
)
@login_required
def follow_user(user_id):

    try:

        FollowService.follow_user(
            session["user_id"],
            user_id
        )

        flash(
            "User followed successfully.",
            "success"
        )

    except ValueError as error:

        flash(str(error), "danger")

    return redirect(
        url_for("home.home")
    )


# ==================== JINJA UNFOLLOW ====================

@follow_bp.route(
    "/users/<int:user_id>/unfollow",
    methods=["POST"]
)
@login_required
def unfollow_user_html(user_id):

    try:

        FollowService.unfollow_user(
            session["user_id"],
            user_id
        )

        flash(
            "User unfollowed successfully.",
            "success"
        )

    except ValueError as error:

        flash(str(error), "danger")

    return redirect(
        url_for("home.home")
    )

