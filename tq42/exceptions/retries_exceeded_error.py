from tq42.exceptions.tq42_api_error import TQ42APIError


class ExceedRetriesError(TQ42APIError):
    def __init__(self, tries: int):
        self.tries = tries

    def __str__(self):
        return "Polling exceeded. Number of retries: {}".format(self.tries)
