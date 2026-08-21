from datetime import datetime

from app import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    recipient_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    actor_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    type = db.Column(
        db.String(30),
        nullable=False
    )

    post_id = db.Column(
        db.BigInteger,
        db.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=True
    )

    comment_id = db.Column(
        db.BigInteger,
        db.ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True
    )

    is_read = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.Index(
            "idx_notifications_recipient",
            "recipient_id",
            "is_read",
            "created_at"
        ),
    )
    recipient = db.relationship(
        "User",
        foreign_keys=[recipient_id],
        back_populates="received_notifications"
    )

    actor = db.relationship(
        "User",
        foreign_keys=[actor_id],
        back_populates="sent_notifications"
    )

    post = db.relationship(
        "Post",
        foreign_keys=[post_id]
    )

    comment = db.relationship(
        "Comment",
        foreign_keys=[comment_id]
    )