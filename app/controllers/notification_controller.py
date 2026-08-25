from flask import Blueprint, jsonify, render_template, redirect, url_for, session, flash

from app.services.notification_service import NotificationService


notification_bp = Blueprint(
    "notification",
    __name__,
    url_prefix="/notifications"
)


@notification_bp.route("/", methods=["GET"])
def notifications():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login"))

    notifications = NotificationService.get_user_notifications(
        user_id
    )

    return render_template(
        "notifications.html",
        notifications=notifications
    )


@notification_bp.route(
    "/<int:notification_id>/read",
    methods=["POST"]
)
def mark_notification_as_read_html(notification_id):

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login"))

    try:

        NotificationService.mark_as_read(
            notification_id,
            user_id
        )

        flash(
            "Notification marked as read.",
            "success"
        )

    except ValueError as e:

        flash(str(e), "error")

    except PermissionError as e:

        flash(str(e), "error")

    return redirect(
        url_for("notification.notifications")
    )


@notification_bp.route(
    "/read-all",
    methods=["POST"]
)
def mark_all_as_read_html():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login"))

    NotificationService.mark_all_as_read(
        user_id
    )

    flash(
        "All notifications marked as read.",
        "success"
    )

    return redirect(
        url_for("notification.notifications")
    )


@notification_bp.route(
    "/<int:notification_id>/delete",
    methods=["POST"]
)
def delete_notification_html(notification_id):

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login"))

    try:

        NotificationService.delete_notification(
            notification_id,
            user_id
        )

        flash(
            "Notification deleted.",
            "success"
        )

    except ValueError as e:

        flash(str(e), "error")

    except PermissionError as e:

        flash(str(e), "error")

    return redirect(
        url_for("notification.notifications")
    )