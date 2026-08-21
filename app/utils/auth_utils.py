from functools import wraps

from flask import session, redirect, url_for, flash, jsonify
from flask_jwt_extended import get_jwt, jwt_required


def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            flash("Please login first.", "danger")

            return redirect(url_for("auth.login"))

        return function(*args, **kwargs)

    return wrapper


def has_any_role(*allowed_roles):
    """Return whether the authenticated JWT role is one of allowed_roles."""
    return get_jwt().get("role") in allowed_roles


def role_required(*required_roles):
    """Require a JWT whose role claim is one of the allowed application roles."""

    if not required_roles:
        raise ValueError("At least one role is required.")

    def decorator(function):

        @wraps(function)
        @jwt_required()
        def wrapper(*args, **kwargs):

            if not has_any_role(*required_roles):

                return jsonify({
                    "error": "Access denied."
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator
