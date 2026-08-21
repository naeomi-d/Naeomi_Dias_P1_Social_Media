from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.api.v1.common import current_user_id, error_response, serialize_comment
from app.services.comment_service import CommentService
from app.services.post_service import PostService


comment_api_bp = Blueprint("comment_api", __name__, url_prefix="/api/v1")


@comment_api_bp.get("/posts/<int:post_id>/comments")
@jwt_required()
def get_post_comments(post_id):
    try:
        comments = CommentService.get_comments_for_post(post_id, current_user_id())
        return jsonify({"comments": [serialize_comment(comment) for comment in comments]}), 200
    except ValueError as error:
        return error_response(str(error), 404)
    except PermissionError as error:
        return error_response(str(error), 403)


@comment_api_bp.post("/posts/<int:post_id>/comments")
@jwt_required()
def create_comment(post_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("A JSON request body is required.", 400)
    try:
        PostService.get_post_for_viewer(post_id, current_user_id())
        comment = CommentService.add_comment(current_user_id(), post_id, data.get("content"))
        return jsonify({"message": "Comment created successfully.", "comment": serialize_comment(comment)}), 201
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 422)
    except PermissionError as error:
        return error_response(str(error), 403)


@comment_api_bp.get("/comments/<int:comment_id>")
@jwt_required()
def get_comment(comment_id):
    try:
        return jsonify({"comment": serialize_comment(CommentService.get_comment(comment_id))}), 200
    except ValueError as error:
        return error_response(str(error), 404)


@comment_api_bp.patch("/comments/<int:comment_id>")
@jwt_required()
def update_comment(comment_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return error_response("A JSON request body is required.", 400)
    try:
        comment = CommentService.update_comment(comment_id, current_user_id(), data.get("content"))
        return jsonify({"message": "Comment updated successfully.", "comment": serialize_comment(comment)}), 200
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 422)
    except PermissionError as error:
        return error_response(str(error), 403)


@comment_api_bp.delete("/comments/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id):
    try:
        CommentService.delete_comment(comment_id, current_user_id())
        return "", 204
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 409)
    except PermissionError as error:
        return error_response(str(error), 403)
