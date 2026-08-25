from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.services.auth_service import AuthService
from app import limiter


auth_api_bp = Blueprint(
    "auth_api",
    __name__,
    url_prefix="/api/v1/auth"
)


@auth_api_bp.route("/register", methods=["POST"])
def api_register():
    """
    Register a new user.

    ---
    tags:
      - Authentication

    consumes:
      - application/json

    produces:
      - application/json

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
            - first_name
            - last_name
          properties:
            username:
              type: string
              example: new_user
            email:
              type: string
              example: newuser@example.com
            password:
              type: string
              example: Password123!
            first_name:
              type: string
              example: New
            last_name:
              type: string
              example: User

    responses:
      201:
        description: Registration successful.

      400:
        description: Request body or required fields are missing.

      422:
        description: Username already exists.
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body is required."}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    if not username or not email or not password or not first_name or not last_name:
        return jsonify({"error": "All registration fields are required."}), 400

    try:
        user = AuthService.register(username, email, password, first_name, last_name)
        return jsonify({
            "message": "Registration successful.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role
            }
        }), 201
    except ValueError as error:
        return jsonify({"error": str(error)}), 422


@auth_api_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def api_login():
    """
    Authenticate a user and return a JWT access token.

    ---
    tags:
      - Authentication

    consumes:
      - application/json

    produces:
      - application/json

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: p1_admin
            password:
              type: string
              example: AdminPassword123

    responses:
      200:
        description: Login successful. Returns a JWT access token.

      400:
        description: Request body or login credentials are missing.

      401:
        description: Invalid username/password or inactive account.

      429:
        description: Too many login attempts.
    """
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body is required."}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    try:
        user = AuthService.login(username, password)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
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
        return jsonify({"error": str(error)}), 401

    
