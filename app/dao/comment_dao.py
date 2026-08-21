from app import db
from app.models.comment import Comment


class CommentDAO:

    @staticmethod
    def create(comment):

        db.session.add(comment)
        db.session.commit()

        return comment

    @staticmethod
    def find_by_id(comment_id):

        return Comment.query.filter_by(
            id=comment_id
        ).first()

    @staticmethod
    def update(comment):
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def find_active_by_post(post_id):

        return (
            Comment.query
            .filter_by(
                post_id=post_id,
                deleted_at=None
            )
            .order_by(Comment.created_at.asc())
            .all()
        )

    @staticmethod
    def find_by_user(user_id):
        return (
            Comment.query
            .filter_by(user_id=user_id, deleted_at=None)
            .order_by(Comment.created_at.desc())
            .all()
        )
