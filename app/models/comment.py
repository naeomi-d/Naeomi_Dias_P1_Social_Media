from datetime import datetime

from app import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    post_id = db.Column(
        db.BigInteger,
        db.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    content = db.Column(
        db.Text,
        nullable=False
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

    post = db.relationship(
        "Post",
        back_populates="comments"
    )

    user = db.relationship(
        "User",
        back_populates="comments"
    )