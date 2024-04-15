from tq42.utils.file_handling import read_file
from tq42.utils.constants import (
    insufficient_permission_errors_file,
    invalid_arguments_error_file,
    no_default_error_file,
    unauthenticated_error_file,
    local_permission_error_file,
)


class TQ42APIError(Exception):
    """Base class for custom exceptions in TQ42API."""

    pass


class ExceedRetriesError(TQ42APIError):
    def __init__(self, tries: int):
        self.tries = tries

    def __str__(self):
        return "Polling exceeded. Number of retries: {}".format(self.tries)


class NoDefaultError(TQ42APIError):
    def __init__(self, command: str):
        self.command = command

    def __str__(self):
        return read_file(no_default_error_file).format(self.command)


class InvalidArgumentError(TQ42APIError):
    def __init__(self, command: str, details: str):
        self.command = command
        self.details = details

    def __str__(self):
        return read_file(invalid_arguments_error_file).format(
            self.command, self.details
        )


class UnauthenticatedError(TQ42APIError):
    def __str__(self):
        return read_file(unauthenticated_error_file)


class PermissionDeniedError(TQ42APIError):
    def __str__(self):
        return read_file(insufficient_permission_errors_file)


class InvalidInputCliError(TQ42APIError):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return "Invalid input: " + self.msg


class NoMatchingAttributeError(TQ42APIError):
    def __init__(self, details: str):
        self.details = details


class LocalPermissionError(TQ42APIError):
    def __str__(self):
        return read_file(local_permission_error_file)


class ExperimentRunCancelError(TQ42APIError):
    def __str__(self):
        return "Cannot cancel a run that was already completed or cancelled."


class AuthenticationError(TQ42APIError):
    def __init__(self, message="Authentication error occurred."):
        self.message = message
        super().__init__(self.message)
