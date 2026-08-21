from datetime import datetime

from app import db


class Follow(db.Model):
    __tablename__ = "follows"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    follower_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    following_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            "follower_id",
            "following_id",
            name="uq_follows_pair"
        ),
        db.Index(
            "idx_follows_follower",
            "follower_id"
        ),
        db.Index(
            "idx_follows_following",
            "following_id"
        ),
    )

    follower = db.relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following"
    )

    following = db.relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="followers"
    )