from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.services.auth_service import AuthService


auth_api_bp = Blueprint(
    "auth_api",
    __name__,
    url_prefix="/api/v1/auth"
)


@auth_api_bp.route("/login", methods=["POST"])
def api_login():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body is required."
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required."
        }), 400

    try:

        user = AuthService.login(
            username,
            password
        )

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        return jsonify({
            "message": "Login successful.",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 401
