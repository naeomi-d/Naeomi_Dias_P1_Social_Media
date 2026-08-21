from app import db
from app.models.like import Like


class LikeDAO:

    @staticmethod
    def find_by_user_and_post(user_id, post_id):

        return Like.query.filter_by(
            user_id=user_id,
            post_id=post_id
        ).first()

    @staticmethod
    def create(like):

        db.session.add(like)
        db.session.commit()

        return like

    @staticmethod
    def delete(like):

        db.session.delete(like)
        db.session.commit()

    @staticmethod
    def count_by_post(post_id):

        return Like.query.filter_by(
            post_id=post_id
        ).count()

    @staticmethod
    def find_by_post(post_id):
        return (
            Like.query.filter_by(post_id=post_id)
            .order_by(Like.created_at.desc())
            .all()
        )

    @staticmethod
    def find_by_user(user_id):
        return (
            Like.query.filter_by(user_id=user_id)
            .order_by(Like.created_at.desc())
            .all()
        )
