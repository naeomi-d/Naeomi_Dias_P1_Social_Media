from flask import (Blueprint,render_template,
                   request,redirect,url_for,flash,session)

from app.services.post_service import PostService
from app.utils.auth_utils import login_required
from app.services.like_service import LikeService
from app.services.comment_service import CommentService


post_bp = Blueprint("post", __name__)


@post_bp.route("/posts/<int:post_id>", methods=["GET"])
@login_required
def post_detail(post_id):
    try:
        post = PostService.get_post_for_viewer(post_id, session["user_id"])
        return render_template("post_detail.html", post=post)
    except (ValueError, PermissionError) as error:
        flash(str(error), "danger")
        return redirect(url_for("home.home"))


@post_bp.route("/posts/create", methods=["GET", "POST"])
@login_required
def create_post():

    if request.method == "POST":

        content = request.form.get("content")
        visibility = request.form.get("visibility")

        try:

            PostService.create_post(
                session["user_id"],
                content,
                visibility
            )

            flash("Post created successfully.", "success")

            return redirect(url_for("home.home"))

        except ValueError as error:

            flash(str(error), "danger")

    return render_template("create_post.html")

@post_bp.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):

    try:
        post = PostService.get_post_for_viewer(
            post_id,
            session["user_id"]
        )
    except ValueError:
        flash("Post not found.", "danger")
        return redirect(url_for("home.home"))
    except PermissionError:
        flash("You cannot edit this post.", "danger")
        return redirect(url_for("home.home"))

    if post.user_id != session["user_id"]:
        flash("You cannot edit this post.", "danger")
        return redirect(url_for("home.home"))

    if request.method == "POST":

        content = request.form.get("content")
        visibility = request.form.get("visibility")

        try:

            PostService.update_post(
                post_id,
                session["user_id"],
                content,
                visibility
            )

            flash("Post updated successfully.", "success")

            return redirect(url_for("home.home"))

        except (ValueError, PermissionError) as error:

            flash(str(error), "danger")

    return render_template(
        "edit_post.html",
        post=post
    )

@post_bp.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):

    try:

        PostService.delete_post(
            post_id,
            session["user_id"]
        )

        flash("Post deleted successfully.", "success")

    except (ValueError, PermissionError) as error:

        flash(str(error), "danger")

    return redirect(url_for("home.home"))

@post_bp.route(
    "/posts/<int:post_id>/like",
    methods=["POST"]
)
@login_required
def like_post(post_id):

    try:

        LikeService.like_post(
            session["user_id"],
            post_id
        )

        flash("Post liked.", "success")

    except ValueError as error:

        flash(str(error), "danger")

    return redirect(url_for("home.home"))

@post_bp.route(
    "/posts/<int:post_id>/unlike",
    methods=["POST"]
)
@login_required
def unlike_post(post_id):

    try:

        LikeService.unlike_post(
            session["user_id"],
            post_id
        )

        flash("Post unliked.", "success")

    except ValueError as error:

        flash(str(error), "danger")

    return redirect(url_for("home.home"))

@post_bp.route(
    "/posts/<int:post_id>/comments",
    methods=["POST"]
)
@login_required
def add_comment(post_id):

    content = request.form.get("content")

    try:

        CommentService.add_comment(
            session["user_id"],
            post_id,
            content
        )

        flash("Comment added.", "success")

    except ValueError as error:

        flash(str(error), "danger")

    return redirect(url_for("home.home"))

@post_bp.route(
    "/comments/<int:comment_id>/delete",
    methods=["POST"]
)
@login_required
def delete_comment(comment_id):

    try:

        CommentService.delete_comment(
            comment_id,
            session["user_id"]
        )

        flash("Comment deleted.", "success")

    except (ValueError, PermissionError) as error:

        flash(str(error), "danger")

    return redirect(url_for("home.home"))
