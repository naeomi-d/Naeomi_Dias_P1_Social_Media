from app.exceptions.base import AppException


class ResourceNotFoundError(AppException):
    
    status_code = 404
    message = "Resource not found."