from flask import jsonify
from flask_jwt_extended import get_jwt_identity


def current_user_id():
    return int(get_jwt_identity())


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def serialize_user(user, include_email=False):
    data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user.bio,
        "profile_picture": user.profile_picture,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat(),
    }
    if include_email:
        data["email"] = user.email
    return data


def serialize_post(post):
    return {
        "id": post.id,
        "user_id": post.user_id,
        "content": post.content,
        "image_path": post.image_path,
        "visibility": post.visibility,
        "status": post.status,
        "created_at": post.created_at.isoformat(),
        "updated_at": post.updated_at.isoformat(),
    }


def serialize_comment(comment):
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "user_id": comment.user_id,
        "content": comment.content,
        "created_at": comment.created_at.isoformat(),
        "updated_at": comment.updated_at.isoformat(),
    }


def serialize_like(like):
    return {
        "id": like.id,
        "user_id": like.user_id,
        "post_id": like.post_id,
        "created_at": like.created_at.isoformat(),
    }


def serialize_follow(follow):
    return {
        "id": follow.id,
        "follower_id": follow.follower_id,
        "following_id": follow.following_id,
        "created_at": follow.created_at.isoformat(),
    }


def serialize_bookmark(bookmark):
    return {
        "id": bookmark.id,
        "user_id": bookmark.user_id,
        "post_id": bookmark.post_id,
        "created_at": bookmark.created_at.isoformat(),
    }


def serialize_hashtag(hashtag):
    return {
        "id": hashtag.id,
        "name": hashtag.name,
        "created_at": hashtag.created_at.isoformat(),
    }


def serialize_report(report):
    return {
        "id": report.id,
        "reporter_id": report.reporter_id,
        "reported_user_id": report.reported_user_id,
        "post_id": report.post_id,
        "reason": report.reason,
        "description": report.description,
        "status": report.status,
        "reviewed_by": report.reviewed_by,
        "reviewed_at": report.reviewed_at.isoformat() if report.reviewed_at else None,
        "created_at": report.created_at.isoformat(),
    }


def serialize_audit_log(audit_log):
    return {
        "id": audit_log.id,
        "admin_id": audit_log.admin_id,
        "action": audit_log.action,
        "entity_type": audit_log.entity_type,
        "entity_id": audit_log.entity_id,
        "details": audit_log.details,
        "created_at": audit_log.created_at.isoformat(),
    }
