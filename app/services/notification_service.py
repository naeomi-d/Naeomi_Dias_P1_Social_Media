from app.models.notification import Notification

from app.dao.notification_dao import NotificationDAO


class NotificationService:

    VALID_TYPES = {
        "LIKE",
        "COMMENT",
        "FOLLOW",
        "MENTION"
    }


    @staticmethod
    def create_notification(
        recipient_id,
        actor_id,
        notification_type,
        post_id=None,
        comment_id=None
    ):

        if notification_type not in NotificationService.VALID_TYPES:
            raise ValueError(
                "Invalid notification type."
            )

        if recipient_id == actor_id:
            return None

        notification = Notification(
            recipient_id=recipient_id,
            actor_id=actor_id,
            type=notification_type,
            post_id=post_id,
            comment_id=comment_id,
            is_read=False
        )

        return NotificationDAO.create(notification)


    @staticmethod
    def get_user_notifications(recipient_id):

        return NotificationDAO.find_by_recipient(
            recipient_id
        )


    @staticmethod
    def get_unread_notifications(recipient_id):

        return NotificationDAO.find_unread_by_recipient(
            recipient_id
        )


    @staticmethod
    def mark_as_read(
        notification_id,
        recipient_id
    ):

        notification = NotificationDAO.find_by_id(
            notification_id
        )

        if not notification:
            raise ValueError(
                "Notification not found."
            )

        if notification.recipient_id != recipient_id:
            raise PermissionError(
                "You cannot modify this notification."
            )

        return NotificationDAO.mark_as_read(
            notification
        )


    @staticmethod
    def mark_all_as_read(recipient_id):

        return NotificationDAO.mark_all_as_read(
            recipient_id
        )


    @staticmethod
    def delete_notification(
        notification_id,
        recipient_id
    ):

        notification = NotificationDAO.find_by_id(
            notification_id
        )

        if not notification:
            raise ValueError(
                "Notification not found."
            )

        if notification.recipient_id != recipient_id:
            raise PermissionError(
                "You cannot delete this notification."
            )

        NotificationDAO.delete(notification)