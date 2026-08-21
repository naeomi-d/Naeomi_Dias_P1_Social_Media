from app import db
from app.models.bookmark import Bookmark


class BookmarkDAO:

    @staticmethod
    def find_by_user_and_post(user_id, post_id):

        return Bookmark.query.filter_by(
            user_id=user_id,
            post_id=post_id
        ).first()

    @staticmethod
    def create(bookmark):

        db.session.add(bookmark)
        db.session.commit()

        return bookmark

    @staticmethod
    def delete(bookmark):

        db.session.delete(bookmark)
        db.session.commit()

    @staticmethod
    def find_by_user(user_id):

        return (
            Bookmark.query
            .filter_by(user_id=user_id)
            .order_by(Bookmark.created_at.desc())
            .all()
        )

    @staticmethod
    def find_by_id(bookmark_id):
        return Bookmark.query.filter_by(id=bookmark_id).first()
