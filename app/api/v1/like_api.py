from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.api.v1.common import current_user_id, error_response, serialize_like
from app.services.like_service import LikeService
from app.services.post_service import PostService


like_api_bp = Blueprint("like_api", __name__, url_prefix="/api/v1")


@like_api_bp.post("/posts/<int:post_id>/likes")
@jwt_required()
def like_post(post_id):
    try:
        PostService.get_post_for_viewer(post_id, current_user_id())
        like = LikeService.like_post(current_user_id(), post_id)
        return jsonify({"message": "Post liked successfully.", "like": serialize_like(like)}), 201
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 409)
    except PermissionError as error:
        return error_response(str(error), 403)


@like_api_bp.delete("/posts/<int:post_id>/likes/me")
@jwt_required()
def unlike_post(post_id):
    try:
        LikeService.unlike_post(current_user_id(), post_id)
        return "", 204
    except ValueError as error:
        return error_response(str(error), 409)


@like_api_bp.get("/posts/<int:post_id>/likes")
@jwt_required()
def get_post_likes(post_id):
    try:
        PostService.get_post_for_viewer(post_id, current_user_id())
        return jsonify({"likes": [serialize_like(like) for like in LikeService.get_post_likes(post_id)]}), 200
    except ValueError as error:
        return error_response(str(error), 404)
    except PermissionError as error:
        return error_response(str(error), 403)


@like_api_bp.get("/posts/<int:post_id>/likes/count")
@jwt_required()
def get_like_count(post_id):
    try:
        PostService.get_post_for_viewer(post_id, current_user_id())
        return jsonify({"post_id": post_id, "like_count": LikeService.get_like_count(post_id)}), 200
    except ValueError as error:
        return error_response(str(error), 404)
    except PermissionError as error:
        return error_response(str(error), 403)


@like_api_bp.get("/likes/me")
@jwt_required()
def get_current_user_likes():
    return jsonify({"likes": [serialize_like(like) for like in LikeService.get_user_likes(current_user_id())]}), 200


@like_api_bp.get("/posts/<int:post_id>/like-status")
@jwt_required()
def get_like_status(post_id):
    try:
        PostService.get_post_for_viewer(post_id, current_user_id())
        like = LikeService.get_like_status(current_user_id(), post_id)
        return jsonify({"liked": like is not None, "like": serialize_like(like) if like else None}), 200
    except ValueError as error:
        return error_response(str(error), 404)
    except PermissionError as error:
        return error_response(str(error), 403)
