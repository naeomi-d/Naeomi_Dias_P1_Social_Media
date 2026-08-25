from app.dao.user_dao import UserDAO
from app.services.file_service import FileService
from app.services.follow_service import FollowService

from app.exceptions.resource_exceptions import ResourceNotFoundError
from app.exceptions.validation_exceptions import ValidationError


class UserService:

    @staticmethod
    def get_users():
        """
        Return all users.

        Used by administrative functionality.
        Includes inactive users.
        """
        return UserDAO.find_all()

    @staticmethod
    def get_paginated_users(page=1, per_page=20):
        """
        Admin user listing.

        Includes both active and inactive users.
        """
        return UserDAO.find_paginated(
            page=page,
            per_page=per_page
        )

    @staticmethod
    def get_user_count():
        return UserDAO.count_all()

    @staticmethod
    def get_active_user_count():
        return UserDAO.count_active()

    @staticmethod
    def get_inactive_user_count():
        return UserDAO.count_inactive()

    @staticmethod
    def get_role_count(role):
        return UserDAO.count_by_role(role)

    @staticmethod
    def update_user_record(user):
        return UserDAO.update(user)

    @staticmethod
    def get_user(user_id):

        user = UserDAO.find_by_id(user_id)

        if not user:
            raise ResourceNotFoundError(
                "User not found."
            )

        return user

    @staticmethod
    def get_active_users(current_user_id=None):

        return UserDAO.find_active_users(
            current_user_id
        )

    @staticmethod
    def get_recent_users(limit=6):

        return UserDAO.find_recent_users(
            limit
        )

    @staticmethod
    def get_profile(user_id):

        user = UserService.get_user(user_id)

        
        if not user.is_active:
            raise ResourceNotFoundError(
                "User not found."
            )

        return user, {
            "followers": FollowService.get_follower_count(
                user_id
            ),
            "following": FollowService.get_following_count(
                user_id
            ),
        }

   
    @staticmethod
    def update_profile(user_id, data):

        user = UserService.get_user(user_id)

        allowed_fields = {
            "first_name",
            "last_name",
            "bio",
            "profile_picture"
        }

        if not any(
            field in data
            for field in allowed_fields
        ):
            raise ValidationError(
                "Provide at least one editable profile field."
            )

        for field in allowed_fields:

            if field in data:

                value = data[field]

                if field in {
                    "first_name",
                    "last_name"
                } and (
                    value is None
                    or not str(value).strip()
                ):

                    raise ValidationError(
                        f"{field.replace('_', ' ').title()} "
                        "cannot be empty."
                    )

                setattr(
                    user,
                    field,
                    str(value).strip()
                    if value is not None
                    else None
                )

        return UserDAO.update(user)

   
    @staticmethod
    def update_avatar(user_id, image_file):

        user = UserService.get_user(user_id)

        if not image_file or not image_file.filename:

            raise ValueError(
                "An image file is required."
            )

        old_picture = user.profile_picture

        new_path = FileService.save_upload(
            image_file,
            "profile_pictures"
        )

        try:

            user.profile_picture = new_path

            UserDAO.update(user)

        except Exception:

            FileService.cleanup_file(
                new_path
            )

            raise

        if (
            old_picture
            and old_picture != new_path
        ):

            FileService.cleanup_file(
                old_picture
            )

        return user

    @staticmethod
    def search_users(
        search_term,
        current_user_id
    ):

        if (
            not search_term
            or not search_term.strip()
        ):

            return UserDAO.find_active_users(
                current_user_id
            )

        return UserDAO.search_users(
            search_term,
            current_user_id
        )