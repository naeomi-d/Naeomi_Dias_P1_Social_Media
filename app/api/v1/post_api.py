from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.api.v1.common import current_user_id, error_response, serialize_post
from app.services.post_service import PostService


post_api_bp = Blueprint("post_api", __name__, url_prefix="/api/v1/posts")


@post_api_bp.get("")
@jwt_required()
def get_posts():
    posts = PostService.get_feed(current_user_id())
    return jsonify({"posts": [serialize_post(post) for post in posts]}), 200


@post_api_bp.post("")
@jwt_required()
def create_post():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("A JSON request body is required.", 400)
    try:
        post = PostService.create_post(
            current_user_id(), data.get("content"), data.get("visibility", "PUBLIC")
        )
        return jsonify({"message": "Post created successfully.", "post": serialize_post(post)}), 201
    except ValueError as error:
        return error_response(str(error), 422)


@post_api_bp.get("/<int:post_id>")
@jwt_required()
def get_post(post_id):
    try:
        return jsonify({"post": serialize_post(PostService.get_post_for_viewer(post_id, current_user_id()))}), 200
    except ValueError as error:
        return error_response(str(error), 404)
    except PermissionError as error:
        return error_response(str(error), 403)


@post_api_bp.patch("/<int:post_id>")
@jwt_required()
def update_post(post_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("A JSON request body is required.", 400)
    if "content" not in data and "visibility" not in data:
        return error_response("Provide content and/or visibility to update.", 422)
    try:
        post = PostService.update_post(
            post_id, current_user_id(), data.get("content"), data.get("visibility")
        )
        return jsonify({"message": "Post updated successfully.", "post": serialize_post(post)}), 200
    except ValueError as error:
        return error_response(str(error), 422 if "not found" not in str(error).lower() else 404)
    except PermissionError as error:
        return error_response(str(error), 403)


@post_api_bp.delete("/<int:post_id>")
@jwt_required()
def delete_post(post_id):
    try:
        PostService.delete_post(post_id, current_user_id())
        return "", 204
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 409)
    except PermissionError as error:
        return error_response(str(error), 403)
