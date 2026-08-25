from app import db
from app.models.follow import Follow


class FollowDAO:

    @staticmethod
    def find_follow(follower_id, following_id):

        return Follow.query.filter_by(
            follower_id=follower_id,
            following_id=following_id
        ).first()

    @staticmethod
    def create(follow):

        db.session.add(follow)
        db.session.commit()

        return follow

    @staticmethod
    def delete(follow):

        db.session.delete(follow)
        db.session.commit()

    @staticmethod
    def get_followers(user_id):

        follows = (
            Follow.query
            .filter_by(following_id=user_id)
            .all()
        )

        return [
            follow.follower
            for follow in follows
        ]

    @staticmethod
    def get_following(user_id):

        follows = (
            Follow.query
            .filter_by(follower_id=user_id)
            .all()
        )

        return [
            follow.following
            for follow in follows
        ]

    @staticmethod
    def count_followers(user_id):

        return Follow.query.filter_by(
            following_id=user_id
        ).count()

    @staticmethod
    def count_following(user_id):

        return Follow.query.filter_by(
            follower_id=user_id
        ).count()