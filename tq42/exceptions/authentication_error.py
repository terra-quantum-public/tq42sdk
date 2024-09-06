from tq42.exceptions.tq42_api_error import TQ42APIError


class AuthenticationError(TQ42APIError):
    """
    Raised when an error occurs during authentication.
    """

    def __init__(self):
        super().__init__("No access token can be retrieved from the response.")
