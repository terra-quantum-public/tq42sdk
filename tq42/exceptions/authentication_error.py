from tq42.exceptions.tq42_api_error import TQ42APIError


class AuthenticationError(TQ42APIError):
    """
    Raised when an error occurs during authentication.

    Attributes:
        message (str): exact reason for the error
    """

    def __init__(self, message="Authentication error occurred."):
        self.message = message
        super().__init__(self.message)
