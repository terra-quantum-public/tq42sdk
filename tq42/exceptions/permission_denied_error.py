from tq42.exceptions.tq42_api_error import TQ42APIError

_MESSAGE = """
Unauthorized Access: Insufficient Permissions
You do not have the necessary privileges to execute the requested command. Double check that the resource exists and contact your system administrator or request the appropriate access level.
Suggestions:
Verify that you have the required permissions to perform the command.
If you believe you should have access, contact your system administrator or request the necessary privileges.
Ensure that you are logged in with the correct user account.
""".strip()


class PermissionDeniedError(TQ42APIError):
    """
    Raised when the user does not have access to the requested resource
    """

    def __str__(self):
        return _MESSAGE
