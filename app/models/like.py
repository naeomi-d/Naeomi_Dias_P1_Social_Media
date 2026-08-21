from datetime import datetime

from app import db


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    post_id = db.Column(
        db.BigInteger,
        db.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "post_id",
            name="uq_likes_user_post"
        ),
        db.Index(
            "idx_likes_post",
            "post_id"
        ),
        db.Index(
            "idx_likes_user",
            "user_id"
        ),
    )

    user = db.relationship(
        "User",
        back_populates="likes"
    )

    post = db.relationship(
        "Post",
        back_populates="likes"
    )