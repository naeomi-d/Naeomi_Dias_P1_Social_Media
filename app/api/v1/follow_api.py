from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.api.v1.common import current_user_id, error_response, serialize_follow
from app.services.follow_service import FollowService


follow_api_bp = Blueprint("follow_api", __name__, url_prefix="/api/v1/users")


@follow_api_bp.post("/<int:user_id>/followers")
@jwt_required()
def follow_user(user_id):
    try:
        follow = FollowService.follow_user(current_user_id(), user_id)
        return jsonify({"message": "User followed successfully.", "follow": serialize_follow(follow)}), 201
    except ValueError as error:
        return error_response(str(error), 404 if "not found" in str(error).lower() else 409)


@follow_api_bp.delete("/<int:user_id>/followers/me")
@jwt_required()
def unfollow_user(user_id):
    try:
        FollowService.unfollow_user(current_user_id(), user_id)
        return "", 204
    except ValueError as error:
        return error_response(str(error), 409)


@follow_api_bp.get("/<int:user_id>/followers")
@jwt_required()
def get_followers(user_id):
    try:
        return jsonify({"followers": [serialize_follow(follow) for follow in FollowService.get_followers(user_id)]}), 200
    except ValueError as error:
        return error_response(str(error), 404)


@follow_api_bp.get("/<int:user_id>/following")
@jwt_required()
def get_following(user_id):
    try:
        return jsonify({"following": [serialize_follow(follow) for follow in FollowService.get_following(user_id)]}), 200
    except ValueError as error:
        return error_response(str(error), 404)


@follow_api_bp.get("/<int:user_id>/follow-status")
@jwt_required()
def get_follow_status(user_id):
    try:
        follow = FollowService.get_follow_status(current_user_id(), user_id)
        return jsonify({"following": follow is not None, "follow": serialize_follow(follow) if follow else None}), 200
    except ValueError as error:
        return error_response(str(error), 404)
