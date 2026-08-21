from app.dao.user_dao import UserDAO
from app.services.follow_service import FollowService


class UserService:

    @staticmethod
    def get_users():
        return UserDAO.find_all()

    @staticmethod
    def get_user(user_id):
        user = UserDAO.find_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        return user

    @staticmethod
    def update_profile(user_id, data):
        user = UserService.get_user(user_id)
        allowed_fields = {"first_name", "last_name", "bio", "profile_picture"}

        if not any(field in data for field in allowed_fields):
            raise ValueError("Provide at least one editable profile field.")

        for field in allowed_fields:
            if field in data:
                value = data[field]
                if field in {"first_name", "last_name"} and (
                    value is None or not str(value).strip()
                ):
                    raise ValueError(f"{field.replace('_', ' ').title()} cannot be empty.")
                setattr(user, field, str(value).strip() if value is not None else None)

        return UserDAO.update(user)

    @staticmethod
    def get_profile(user_id):
        user = UserService.get_user(user_id)
        return user, {
            "followers": FollowService.get_follower_count(user_id),
            "following": FollowService.get_following_count(user_id),
        }
