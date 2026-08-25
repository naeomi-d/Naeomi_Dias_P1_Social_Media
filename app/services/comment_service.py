from datetime import datetime

from app.dao.comment_dao import CommentDAO
from app.dao.post_dao import PostDAO
from app.services.post_service import PostService
from app.models.comment import Comment
from app.services.notification_service import NotificationService

from app.exceptions.resource_exceptions import ResourceNotFoundError
from app.exceptions.validation_exceptions import ValidationError
from app.exceptions.authorization_exceptions import AuthorizationError

class CommentService:

    @staticmethod
    def get_comments_for_post(post_id, viewer_id):
        PostService.get_post_for_viewer(post_id, viewer_id)
        return CommentDAO.find_active_by_post(post_id)

    @staticmethod
    def get_comment(comment_id):
        comment = CommentDAO.find_by_id(comment_id)
        if not comment or comment.deleted_at is not None:
            raise ResourceNotFoundError("Comment not found.")
        return comment

    @staticmethod
    def add_comment(user_id, post_id, content):

        if not content or not content.strip():
            raise ValueError(
                "Comment cannot be empty."
            )

        post = PostDAO.find_by_id(post_id)

        if not post or post.status != "ACTIVE":
            raise ResourceNotFoundError(
                "Post not found."
            )

        comment = Comment(
            user_id=user_id,
            post_id=post_id,
            content=content.strip()
        )

        comment = CommentDAO.create(comment)

        NotificationService.create_notification(
            recipient_id=post.user_id,
            actor_id=user_id,
            notification_type="COMMENT",
            post_id=post_id,
            comment_id=comment.id
        )

        return comment

    @staticmethod
    def update_comment(comment_id, user_id, content):
        comment = CommentService.get_comment(comment_id)

        if comment.user_id != user_id:
            raise AuthorizationError("You cannot edit another user's comment.")

        if not content or not content.strip():
            raise ValidationError("Comment cannot be empty.")

        comment.content = content.strip()
        return CommentDAO.update(comment)

    @staticmethod
    def delete_comment(comment_id, user_id):

        comment = CommentDAO.find_by_id(comment_id)

        if not comment:
            raise ResourceNotFoundError(
                "Comment not found."
            )

        if comment.deleted_at is not None:
            raise ValidationError(
                "Comment has already been deleted."
            )

        if comment.user_id != user_id:
            raise AuthorizationError(
                "You cannot delete another user's comment."
            )

        comment.deleted_at = datetime.utcnow()

        CommentDAO.update(comment)

        return comment
