from tq42.exceptions.tq42_api_error import TQ42APIError


class NoMatchingAttributeError(TQ42APIError):
    def __init__(self, details: str):
        self.details = details
