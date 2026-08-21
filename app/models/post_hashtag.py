from app import db


class PostHashtag(db.Model):
    __tablename__ = "post_hashtags"

    post_id = db.Column(
        db.BigInteger,
        db.ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True
    )

    hashtag_id = db.Column(
        db.BigInteger,
        db.ForeignKey("hashtags.id", ondelete="CASCADE"),
        primary_key=True
    )

    post = db.relationship(
        "Post",
        back_populates="hashtags"
    )

    hashtag = db.relationship(
        "Hashtag",
        back_populates="posts"
    )