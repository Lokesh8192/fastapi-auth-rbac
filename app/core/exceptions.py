class UserNotFoundException(Exception):
    def __init__(self, message: str = "User not found"):
        super().__init__(message)
        self.message = message

class InvalidCredentialsException(Exception):

    def __init__(self):
        self.message = "Invalid credentials"


class RefreshTokenNotFoundException(Exception):

    def __init__(self):
        self.message = "Refresh token not found"