from tq42.exceptions.tq42_api_error import TQ42APIError

_MESSAGE = """
User Not Logged In: Authentication Required
You are not currently logged in. Please log in or authenticate to access this feature or command.
To log in with your username and password or stored token, type the command: tq42 auth login
If you need further assistance, please visit https://help.terraquantum.io/.
""".strip()


class UnauthenticatedError(TQ42APIError):
    """
    Raised when the user is not authenticated
    """

    def __str__(self):
        return _MESSAGE
