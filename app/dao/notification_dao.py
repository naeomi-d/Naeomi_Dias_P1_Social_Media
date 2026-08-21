from app import db

from app.models.notification import Notification


class NotificationDAO:

    @staticmethod
    def create(notification):

        db.session.add(notification)
        db.session.commit()

        return notification


    @staticmethod
    def find_by_id(notification_id):

        return Notification.query.get(notification_id)


    @staticmethod
    def find_by_recipient(recipient_id):

        return Notification.query.filter_by(
            recipient_id=recipient_id
        ).order_by(
            Notification.created_at.desc()
        ).all()


    @staticmethod
    def find_unread_by_recipient(recipient_id):

        return Notification.query.filter_by(
            recipient_id=recipient_id,
            is_read=False
        ).order_by(
            Notification.created_at.desc()
        ).all()


    @staticmethod
    def mark_as_read(notification):

        notification.is_read = True

        db.session.commit()

        return notification


    @staticmethod
    def mark_all_as_read(recipient_id):

        notifications = Notification.query.filter_by(
            recipient_id=recipient_id,
            is_read=False
        ).all()

        for notification in notifications:
            notification.is_read = True

        db.session.commit()

        return notifications


    @staticmethod
    def delete(notification):

        db.session.delete(notification)
        db.session.commit()