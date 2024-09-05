from tq42.exceptions.tq42_api_error import TQ42APIError


class InvalidCLIInputError(TQ42APIError):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"Invalid input: {self.msg}"
