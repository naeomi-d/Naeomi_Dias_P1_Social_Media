from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    session,
    render_template
)

from app.services.bookmark_service import BookmarkService
from app.utils.auth_utils import login_required


bookmark_bp = Blueprint(
    "bookmark",
    __name__
)


@bookmark_bp.route(
    "/posts/<int:post_id>/bookmark",
    methods=["POST"]
)
@login_required
def bookmark_post(post_id):

    try:

        BookmarkService.bookmark_post(
            session["user_id"],
            post_id
        )

        flash(
            "Post bookmarked.",
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


@bookmark_bp.route(
    "/posts/<int:post_id>/unbookmark",
    methods=["POST"]
)
@login_required
def remove_bookmark(post_id):

    try:

        BookmarkService.remove_bookmark(
            session["user_id"],
            post_id
        )

        flash(
            "Bookmark removed.",
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


@bookmark_bp.route(
    "/bookmarks",
    methods=["GET"]
)
@login_required
def my_bookmarks():

    bookmarks = BookmarkService.get_saved_posts(
        session["user_id"]
    )

    return render_template(
        "bookmarks.html",
        bookmarks=bookmarks
    )