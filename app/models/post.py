from datetime import datetime

from app import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    content = db.Column(
        db.Text,
        nullable=True
    )

    image_path = db.Column(
        db.String(500),
        nullable=True
    )

    visibility = db.Column(
        db.String(20),
        nullable=False,
        default="PUBLIC"
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="ACTIVE"
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

    deleted_at = db.Column(
        db.DateTime,
        nullable=True
    )

    user = db.relationship(
        "User",
        back_populates="posts"
    )
    
    comments = db.relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    likes = db.relationship(
        "Like",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    bookmarks = db.relationship(
        "Bookmark",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    hashtags = db.relationship(
        "PostHashtag",
        back_populates="post",
        cascade="all, delete-orphan"
    )
