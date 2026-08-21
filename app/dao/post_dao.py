from app import db
from app.models.post import Post


class PostDAO:

    @staticmethod
    def create(post):
        db.session.add(post)
        return post

    @staticmethod
    def find_by_id(post_id):
        return Post.query.filter_by(id=post_id).first()

    @staticmethod
    def find_active_posts():
        return (
            Post.query
            .filter_by(status="ACTIVE")
            .order_by(Post.created_at.desc())
            .all()
        )

    @staticmethod
    def find_active_by_user(user_id):
        return (
            Post.query
            .filter_by(user_id=user_id, status="ACTIVE")
            .order_by(Post.created_at.desc())
            .all()
        )

    @staticmethod
    def update(post):
        db.session.add(post)
        db.session.commit()
        return post
