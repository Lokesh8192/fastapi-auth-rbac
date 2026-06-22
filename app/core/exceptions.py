class UserNotFoundException(Exception):

    def __init__(self):
        self.message = "User not found"

class InvalidCredentialsException(Exception):

    def __init__(self):
        self.message = "Invalid credentials"


class RefreshTokenNotFoundException(Exception):

    def __init__(self):
        self.message = "Refresh token not found"