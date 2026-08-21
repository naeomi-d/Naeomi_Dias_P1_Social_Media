from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.api.v1.common import current_user_id, error_response, serialize_hashtag, serialize_post
from app.services.hashtag_service import HashtagService


hashtag_api_bp = Blueprint("hashtag_api", __name__, url_prefix="/api/v1")


@hashtag_api_bp.get("/hashtags")
@jwt_required()
def get_hashtags():
    return jsonify({"hashtags": [serialize_hashtag(tag) for tag in HashtagService.get_hashtags()]}), 200


@hashtag_api_bp.get("/hashtags/search")
@jwt_required()
def search_hashtags():
    try:
        tags = HashtagService.search_hashtags(request.args.get("q"))
        return jsonify({"hashtags": [serialize_hashtag(tag) for tag in tags]}), 200
    except ValueError as error:
        return error_response(str(error), 400)


@hashtag_api_bp.get("/hashtags/<string:name>")
@jwt_required()
def get_hashtag(name):
    try:
        return jsonify({"hashtag": serialize_hashtag(HashtagService.get_hashtag(name))}), 200
    except ValueError as error:
        return error_response(str(error), 404)


@hashtag_api_bp.get("/hashtags/<string:name>/posts")
@jwt_required()
def get_hashtag_posts(name):
    try:
        posts = HashtagService.get_posts_for_hashtag(name, current_user_id())
        return jsonify({"posts": [serialize_post(post) for post in posts]}), 200
    except ValueError as error:
        return error_response(str(error), 404)


@hashtag_api_bp.get("/posts/<int:post_id>/hashtags")
@jwt_required()
def get_post_hashtags(post_id):
    try:
        tags = HashtagService.get_post_hashtags(post_id, current_user_id())
        return jsonify({"hashtags": [serialize_hashtag(tag) for tag in tags]}), 200
    except ValueError as error:
        return error_response(str(error), 404)
    except PermissionError as error:
        return error_response(str(error), 403)
