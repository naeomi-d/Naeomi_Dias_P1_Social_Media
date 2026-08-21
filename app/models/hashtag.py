from datetime import datetime

from app import db


class Hashtag(db.Model):
    __tablename__ = "hashtags"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    posts = db.relationship(
        "PostHashtag",
        back_populates="hashtag",
        cascade="all, delete-orphan"
    )