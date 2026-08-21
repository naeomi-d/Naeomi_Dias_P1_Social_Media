from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.api.v1.common import current_user_id, error_response, serialize_bookmark
from app.services.bookmark_service import BookmarkService
from app.services.post_service import PostService


bookmark_api_bp = Blueprint("bookmark_api", __name__, url_prefix="/api/v1")


@bookmark_api_bp.get("/bookmarks")
@jwt_required()
def get_bookmarks():
    bookmarks = BookmarkService.get_saved_posts(current_user_id())
    return jsonify({"bookmarks": [serialize_bookmark(bookmark) for bookmark in bookmarks]}), 200


@bookmark_api_bp.post("/posts/<int:post_id>/bookmarks")
@jwt_required()
def create_bookmark(post_id):
    try:
        PostService.get_post_for_viewer(post_id, current_user_id())
        bookmark = BookmarkService.bookmark_post(current_user_id(), post_id)
        return jsonify({"message": "Post bookmarked successfully.", "bookmark": serialize_bookmark(bookmark)}), 201
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 409)
    except PermissionError as error:
        return error_response(str(error), 403)


@bookmark_api_bp.get("/bookmarks/<int:bookmark_id>")
@jwt_required()
def get_bookmark(bookmark_id):
    try:
        return jsonify({"bookmark": serialize_bookmark(BookmarkService.get_bookmark(bookmark_id, current_user_id()))}), 200
    except ValueError as error:
        return error_response(str(error), 404)
    except PermissionError as error:
        return error_response(str(error), 403)


@bookmark_api_bp.delete("/posts/<int:post_id>/bookmarks/me")
@jwt_required()
def delete_bookmark(post_id):
    try:
        BookmarkService.remove_bookmark(current_user_id(), post_id)
        return "", 204
    except ValueError as error:
        return error_response(str(error), 409)


@bookmark_api_bp.get("/posts/<int:post_id>/bookmark-status")
@jwt_required()
def get_bookmark_status(post_id):
    try:
        bookmark = BookmarkService.get_bookmark_status(current_user_id(), post_id)
        return jsonify({"bookmarked": bookmark is not None, "bookmark": serialize_bookmark(bookmark) if bookmark else None}), 200
    except ValueError as error:
        return error_response(str(error), 404)
