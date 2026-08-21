from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.api.v1.common import current_user_id, error_response, serialize_post, serialize_user
from app.services.post_service import PostService
from app.services.user_service import UserService


user_api_bp = Blueprint("user_api", __name__, url_prefix="/api/v1/users")


@user_api_bp.get("")
@jwt_required()
def get_users():
    return jsonify({"users": [serialize_user(user) for user in UserService.get_users()]}), 200


@user_api_bp.get("/me")
@jwt_required()
def get_current_user():
    return jsonify({"user": serialize_user(UserService.get_user(current_user_id()), True)}), 200


@user_api_bp.patch("/me")
@jwt_required()
def update_current_user():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("A JSON request body is required.", 400)
    try:
        user = UserService.update_profile(current_user_id(), data)
        return jsonify({"message": "Profile updated successfully.", "user": serialize_user(user, True)}), 200
    except ValueError as error:
        return error_response(str(error), 422)


@user_api_bp.post("/me/avatar")
@jwt_required()
def upload_avatar():
    if "avatar" not in request.files and "image" not in request.files:
        return error_response("An image file is required.", 400)
    file_storage = request.files.get("avatar") or request.files.get("image")
    if not file_storage or not file_storage.filename:
        return error_response("An image file is required.", 400)
    try:
        user = UserService.update_avatar(current_user_id(), file_storage)
        return jsonify({"message": "Avatar uploaded successfully.", "user": serialize_user(user, True)}), 200
    except ValueError as error:
        return error_response(str(error), 400)



@user_api_bp.get("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    try:
        return jsonify({"user": serialize_user(UserService.get_user(user_id))}), 200
    except ValueError as error:
        return error_response(str(error), 404)


@user_api_bp.get("/<int:user_id>/profile")
@jwt_required()
def get_user_profile(user_id):
    try:
        user, counts = UserService.get_profile(user_id)
        return jsonify({"user": serialize_user(user), "counts": counts}), 200
    except ValueError as error:
        return error_response(str(error), 404)


@user_api_bp.get("/<int:user_id>/posts")
@jwt_required()
def get_user_posts(user_id):
    try:
        UserService.get_user(user_id)
        posts = PostService.get_user_posts(user_id, current_user_id())
        return jsonify({"posts": [serialize_post(post) for post in posts]}), 200
    except ValueError as error:
        return error_response(str(error), 404)
