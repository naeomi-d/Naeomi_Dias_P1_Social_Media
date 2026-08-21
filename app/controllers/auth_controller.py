from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.auth_service import AuthService


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        

        try:

            user = AuthService.register(
                username,
                email,
                password,
                first_name,
                last_name
            )

            print("USER CREATED:", user.id)

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            flash("Registration successful!", "success")

            return redirect(url_for("home.home"))

        except ValueError as error:

            print("REGISTRATION ERROR:", error)

            flash(str(error), "danger")

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        try:

            user = AuthService.login(username, password)

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role


            flash("Login successful!", "success")

            return redirect(url_for("home.home"))

        except ValueError as error:

            flash(str(error), "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))
