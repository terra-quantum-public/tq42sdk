from tq42.exceptions.tq42_api_error import TQ42APIError


class ExperimentRunCancelError(TQ42APIError):
    """
    Raised when an error occurs while cancelling an experiment run.

    Only raised when the experiment run is either already completed or cancelled.
    """

    def __str__(self):
        return "Cannot cancel a run that was already completed or cancelled."
