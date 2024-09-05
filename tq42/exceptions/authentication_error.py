from tq42.exceptions.tq42_api_error import TQ42APIError


class AuthenticationError(TQ42APIError):
    def __init__(self, message="Authentication error occurred."):
        self.message = message
        super().__init__(self.message)
