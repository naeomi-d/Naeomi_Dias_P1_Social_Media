from app.exceptions.base import AppException


class AuthenticationError(AppException):

    status_code = 401
    message = "Authentication required."