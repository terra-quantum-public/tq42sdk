from tq42.exceptions.tq42_api_error import TQ42APIError


class ExperimentRunCancelError(TQ42APIError):
    def __str__(self):
        return "Cannot cancel a run that was already completed or cancelled."
