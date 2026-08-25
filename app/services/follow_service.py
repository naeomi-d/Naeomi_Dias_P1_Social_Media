from app.dao.follow_dao import FollowDAO
from app.models.follow import Follow
from app.dao.user_dao import UserDAO
from app.services.notification_service import NotificationService

from app.exceptions.resource_exceptions import ResourceNotFoundError
from app.exceptions.validation_exceptions import ValidationError
class FollowService:

    @staticmethod
    def follow_user(follower_id, following_id):

        if follower_id == following_id:
            raise ValidationError(
                "You cannot follow yourself."
            )

        user = UserDAO.find_by_id(following_id)

        if not user:
            raise ResourceNotFoundError(
                "User not found."
            )

        existing_follow = FollowDAO.find_follow(
            follower_id,
            following_id
        )

        if existing_follow:
            raise ValidationError(
                "You are already following this user."
            )

        follow = Follow(
            follower_id=follower_id,
            following_id=following_id
        )

        follow = FollowDAO.create(follow)

        NotificationService.create_notification(
            recipient_id=following_id,
            actor_id=follower_id,
            notification_type="FOLLOW"
        )

        return follow

    @staticmethod
    def unfollow_user(follower_id, following_id):

        existing_follow = FollowDAO.find_follow(
            follower_id,
            following_id
        )

        if not existing_follow:
            raise ValidationError(
                "You are not following this user."
            )

        FollowDAO.delete(existing_follow)

    @staticmethod
    def get_follower_count(user_id):

        return FollowDAO.count_followers(user_id)

    @staticmethod
    def get_following_count(user_id):

        return FollowDAO.count_following(user_id)

    @staticmethod
    def get_followers(user_id):
        if not UserDAO.find_by_id(user_id):
            raise ResourceNotFoundError("User not found.")
        return FollowDAO.get_followers(user_id)

    @staticmethod
    def get_following(user_id):
        if not UserDAO.find_by_id(user_id):
            raise ResourceNotFoundError("User not found.")
        return FollowDAO.get_following(user_id)

    @staticmethod
    def get_follow_status(follower_id, following_id):
        if not UserDAO.find_by_id(following_id):
            raise ResourceNotFoundError("User not found.")
        return FollowDAO.find_follow(follower_id, following_id)
