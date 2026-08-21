from app.dao.like_dao import LikeDAO
from app.dao.post_dao import PostDAO
from app.models.like import Like
from app.services.notification_service import NotificationService


class LikeService:

    @staticmethod
    def like_post(user_id, post_id):

        existing_like = LikeDAO.find_by_user_and_post(
            user_id,
            post_id
        )

        if existing_like:
            raise ValueError(
                "You have already liked this post."
            )

        post = PostDAO.find_by_id(post_id)

        if not post:
            raise ValueError(
                "Post not found."
            )

        like = Like(
            user_id=user_id,
            post_id=post_id
        )

        like = LikeDAO.create(like)

        NotificationService.create_notification(
            recipient_id=post.user_id,
            actor_id=user_id,
            notification_type="LIKE",
            post_id=post_id
        )

        return like

    @staticmethod
    def unlike_post(user_id, post_id):

        like = LikeDAO.find_by_user_and_post(
            user_id,
            post_id
        )

        if not like:
            raise ValueError(
                "You have not liked this post."
            )

        LikeDAO.delete(like)

    @staticmethod
    def get_like_count(post_id):
        post = PostDAO.find_by_id(post_id)
        if not post or post.status != "ACTIVE":
            raise ValueError("Post not found.")
        return LikeDAO.count_by_post(post_id)

    @staticmethod
    def get_post_likes(post_id):
        LikeService.get_like_count(post_id)
        return LikeDAO.find_by_post(post_id)

    @staticmethod
    def get_user_likes(user_id):
        return LikeDAO.find_by_user(user_id)

    @staticmethod
    def get_like_status(user_id, post_id):
        LikeService.get_like_count(post_id)
        return LikeDAO.find_by_user_and_post(user_id, post_id)
