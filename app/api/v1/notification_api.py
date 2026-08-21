from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.notification_service import NotificationService


notification_api_bp = Blueprint(
    "notification_api",
    __name__,
    url_prefix="/api/v1/notifications"
)


def _current_user_id():
    return int(get_jwt_identity())


def _serialize_notification(notification):
    return {
        "id": notification.id,
        "recipient_id": notification.recipient_id,
        "actor_id": notification.actor_id,
        "type": notification.type,
        "post_id": notification.post_id,
        "comment_id": notification.comment_id,
        "is_read": notification.is_read,
        "created_at": notification.created_at.isoformat(),
    }


@notification_api_bp.route(
    "",
    methods=["GET"]
)
@jwt_required()
def get_notifications():

    user_id = _current_user_id()

    notifications = NotificationService.get_user_notifications(
        user_id
    )

    return jsonify({
        "notifications": [
            _serialize_notification(notification)
            for notification in notifications
        ]
    }), 200


@notification_api_bp.route(
    "/unread",
    methods=["GET"]
)
@jwt_required()
def get_unread_notifications():
    notifications = NotificationService.get_unread_notifications(
        _current_user_id()
    )

    return jsonify({
        "notifications": [
            _serialize_notification(notification)
            for notification in notifications
        ]
    }), 200


@notification_api_bp.route(
    "/<int:notification_id>/read",
    methods=["PATCH"]
)
@jwt_required()
def mark_notification_as_read(notification_id):

    user_id = _current_user_id()

    try:

        notification = NotificationService.mark_as_read(
            notification_id,
            user_id
        )

        return jsonify({
            "message": "Notification marked as read.",
            "notification": _serialize_notification(notification)
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except PermissionError as error:

        return jsonify({
            "error": str(error)
        }), 403


@notification_api_bp.route(
    "/read-all",
    methods=["PATCH"]
)
@jwt_required()
def mark_all_notifications_as_read():

    user_id = _current_user_id()

    notifications = NotificationService.mark_all_as_read(
        user_id
    )

    return jsonify({
        "message": "All notifications marked as read.",
        "updated_count": len(notifications)
    }), 200


@notification_api_bp.route(
    "/<int:notification_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_notification(notification_id):

    user_id = _current_user_id()

    try:

        NotificationService.delete_notification(
            notification_id,
            user_id
        )

        return "", 204

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except PermissionError as error:

        return jsonify({
            "error": str(error)
        }), 403
