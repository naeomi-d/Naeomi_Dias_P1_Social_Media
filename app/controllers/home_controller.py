from flask import Blueprint, render_template, session, redirect, url_for, flash, request,send_file

from app.services.post_service import PostService
from app.services.user_service import UserService
from app.utils.auth_utils import login_required
from app.services.file_service import FileService
from app.services.follow_service import FollowService
from app.exceptions.resource_exceptions import ResourceNotFoundError
home_bp = Blueprint("home", __name__)


@home_bp.route("/")
@login_required
def home():

    page = request.args.get("page", 1, type=int)

    users = UserService.get_recent_users(6)

    follow_statuses = {}

    current_user_id = session["user_id"]

    for user in users:

        if user.id == current_user_id:
            continue

        follow_statuses[user.id] = (
            FollowService.get_follow_status(
                current_user_id,
                user.id
            ) is not None
        )

    posts, pagination = PostService.get_feed(
        session["user_id"],
        page=page,
        per_page=10
    )

    return render_template(
        "home.html",
        users=users,
        posts=posts,
        pagination=pagination,
        follow_statuses = follow_statuses
    )


@home_bp.route("/users")
@login_required
def users():

    search_term = request.args.get(
        "search",
        "",
        type=str
    ).strip()

    users = UserService.search_users(
        search_term,
        session["user_id"]
    )

    return render_template(
        "users.html",
        users=users,
        search_term=search_term
    )


@home_bp.route("/users/<int:user_id>")
@login_required
def user_profile(user_id):

    try:

        current_user_id = session["user_id"]

        user, counts = UserService.get_profile(
            user_id
        )

        posts = PostService.get_user_posts(
            user_id,
            current_user_id
        )

        is_following = False

        if user_id != current_user_id:

            is_following = (
                FollowService.get_follow_status(
                    current_user_id,
                    user_id
                )
                is not None
            )

        return render_template(
            "user_profile.html",
            profile_user=user,
            counts=counts,
            posts=posts,
            is_following=is_following
        )

    except (ValueError, ResourceNotFoundError) as error:

        flash(str(error), "danger")

        return redirect(
            url_for("home.users")
        )


@home_bp.route("/profile/avatar", methods=["POST"])
@login_required
def upload_avatar():
    file_storage = request.files.get("avatar") or request.files.get("image")
    try:
        UserService.update_avatar(session["user_id"], file_storage)
        flash("Avatar updated successfully.", "success")
    except ValueError as error:
        flash(str(error), "danger")
    return redirect(url_for("home.user_profile", user_id=session["user_id"]))

@home_bp.route("/uploads/<path:filename>")

def uploaded_file(filename):
    relative_path = f"/uploads/{filename}"

    file_path = FileService.get_safe_file_path(relative_path)

    if not file_path:
        return "File not found.", 404

    try:
        return send_file(file_path)
    except (FileNotFoundError, OSError):
        return "File not found.", 404


@home_bp.route("/users/<int:user_id>/followers")
@login_required
def followers(user_id):

    try:

        current_user_id = session["user_id"]

        profile_user = UserService.get_user(user_id)

        followers = FollowService.get_followers(user_id)

        follow_statuses = {}

        for user in followers:

            if user.id == current_user_id:
                follow_statuses[user.id] = False
                continue

            follow_statuses[user.id] = (
                FollowService.get_follow_status(
                    current_user_id,
                    user.id
                ) is not None
            )

        return render_template(
            "followers.html",
            profile_user=profile_user,
            users=followers,
            follow_statuses=follow_statuses
        )

    except ValueError as error:

        flash(str(error), "danger")

        return redirect(
            url_for("home.users")
        )


@home_bp.route("/users/<int:user_id>/following")
@login_required
def following(user_id):

    try:

        current_user_id = session["user_id"]

        profile_user = UserService.get_user(user_id)

        following_users = FollowService.get_following(user_id)

        follow_statuses = {}

        for user in following_users:

            if user.id == current_user_id:
                follow_statuses[user.id] = False
                continue

            follow_statuses[user.id] = (
                FollowService.get_follow_status(
                    current_user_id,
                    user.id
                ) is not None
            )

        return render_template(
            "following.html",
            profile_user=profile_user,
            users=following_users,
            follow_statuses=follow_statuses
        )

    except ValueError as error:

        flash(str(error), "danger")

        return redirect(
            url_for("home.users")
        )