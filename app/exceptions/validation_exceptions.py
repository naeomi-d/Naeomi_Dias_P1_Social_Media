from app.exceptions.base import AppException


class ValidationError(AppException):
    
    status_code = 422
    message = "Invalid input."