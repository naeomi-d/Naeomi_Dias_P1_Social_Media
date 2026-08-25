from app.dao.bookmark_dao import BookmarkDAO
from app.dao.post_dao import PostDAO
from app.models.bookmark import Bookmark

from app.exceptions.resource_exceptions import ResourceNotFoundError
from app.exceptions.validation_exceptions import ValidationError
from app.exceptions.authorization_exceptions import AuthorizationError

class BookmarkService:

    @staticmethod
    def bookmark_post(user_id, post_id):

        post = PostDAO.find_by_id(post_id)

        if not post:
            raise ResourceNotFoundError("Post not found.")

        if post.status == "DELETED":
            raise ValidationError(
                "Cannot bookmark a deleted post."
            )

        existing_bookmark = (
            BookmarkDAO.find_by_user_and_post(
                user_id,
                post_id
            )
        )

        if existing_bookmark:
            raise ValidationError(
                "Post is already bookmarked."
            )

        bookmark = Bookmark(
            user_id=user_id,
            post_id=post_id
        )

        return BookmarkDAO.create(bookmark)

    @staticmethod
    def remove_bookmark(user_id, post_id):

        bookmark = BookmarkDAO.find_by_user_and_post(
            user_id,
            post_id
        )

        if not bookmark:
            raise ValidationError(
                "Post is not bookmarked."
            )

        BookmarkDAO.delete(bookmark)

    @staticmethod
    def get_saved_posts(user_id):

        return BookmarkDAO.find_by_user(user_id)

    @staticmethod
    def get_bookmark(bookmark_id, user_id):
        bookmark = BookmarkDAO.find_by_id(bookmark_id)
        if not bookmark:
            raise ResourceNotFoundError("Bookmark not found.")
        if bookmark.user_id != user_id:
            raise AuthorizationError("You cannot view another user's bookmark.")
        return bookmark

    @staticmethod
    def get_bookmark_status(user_id, post_id):
        post = PostDAO.find_by_id(post_id)
        if not post or post.status == "DELETED":
            raise ResourceNotFoundError("Post not found.")
        return BookmarkDAO.find_by_user_and_post(user_id, post_id)
