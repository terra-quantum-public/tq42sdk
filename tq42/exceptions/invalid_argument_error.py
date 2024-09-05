from tq42.exceptions.tq42_api_error import TQ42APIError

_MESSAGE = """
Unable to Execute: `{}`

We were unable to execute the given command as it violates certain constraints for the given resource:
{}
""".strip()


class InvalidArgumentError(TQ42APIError):
    def __init__(self, command: str, details: str):
        self.command = command
        self.details = details

    def __str__(self):
        return _MESSAGE.format(self.command, self.details)
