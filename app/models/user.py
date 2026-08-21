from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(255),
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    bio = db.Column(
        db.String(500),
        nullable=True
    )

    profile_picture = db.Column(
        db.String(500),
        nullable=True
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="USER"
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    posts = db.relationship(
        "Post",
        back_populates="user"
    )

    comments = db.relationship(
        "Comment",
        back_populates="user"
    )

    likes = db.relationship(
        "Like",
        back_populates="user"
    )

    following = db.relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower"
    )

    followers = db.relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following"
    )

    bookmarks = db.relationship(
        "Bookmark",
        back_populates="user"
    )
    received_notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.recipient_id",
        back_populates="recipient",
        cascade="all, delete-orphan"
    )

    sent_notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.actor_id",
        back_populates="actor"
    )

    audit_logs = db.relationship(
        "AdminAuditLog",
        foreign_keys="AdminAuditLog.admin_id",
        back_populates="admin"
    )
