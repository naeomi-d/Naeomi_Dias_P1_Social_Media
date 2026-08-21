from flask import Blueprint, render_template, session, redirect, url_for, flash

from app.services.post_service import PostService
from app.services.user_service import UserService
from app.utils.auth_utils import login_required


home_bp = Blueprint("home", __name__)


@home_bp.route("/")
@login_required
def home():

    users = UserService.get_users()
    posts = PostService.get_feed(session["user_id"])

    return render_template(
        "home.html",
        users=users,
        posts=posts
    )


@home_bp.route("/users")
@login_required
def users():
    return render_template("users.html", users=UserService.get_users())


@home_bp.route("/users/<int:user_id>")
@login_required
def user_profile(user_id):
    try:
        user, counts = UserService.get_profile(user_id)
        posts = PostService.get_user_posts(user_id, session["user_id"])
        return render_template(
            "user_profile.html",
            profile_user=user,
            counts=counts,
            posts=posts,
        )
    except ValueError as error:
        flash(str(error), "danger")
        return redirect(url_for("home.users"))
