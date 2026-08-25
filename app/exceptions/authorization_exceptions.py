from app.exceptions.base import AppException


class AuthorizationError(AppException, PermissionError):

    status_code = 403
    message = "You do not have permission to perform this action."