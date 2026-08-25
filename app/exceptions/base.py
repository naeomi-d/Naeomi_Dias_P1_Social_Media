class AppException(Exception):
    
    status_code = 500
    message = "An unexpected application error occurred."

    def __init__(self, message=None, status_code=None):
        self.message = message or self.message

        if status_code is not None:
            self.status_code = status_code

        super().__init__(self.message)