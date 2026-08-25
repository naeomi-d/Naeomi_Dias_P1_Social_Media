import bcrypt

from app.models.user import User
from app.dao.user_dao import UserDAO


class AuthService:

    @staticmethod
    def register(username, email, password, first_name, last_name):

        existing_user = UserDAO.find_by_username(username)

        if existing_user:
            raise ValueError("Username already exists.")

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role="USER"
        )

        return UserDAO.create(user)

    @staticmethod
    def login(username, password):

        user = UserDAO.find_by_username(username)

        if not user:
            raise ValueError("Invalid username or password.")

        password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            user.password_hash.encode("utf-8")
        )

        if not password_matches:
            raise ValueError("Invalid username or password.")

        if not user.is_active:
            raise ValueError("Account is inactive.")

        return user