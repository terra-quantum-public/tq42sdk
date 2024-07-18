import logging
import traceback

from grpc import StatusCode
from grpc._channel import _InactiveRpcError as InactiveRpcError
from grpc.aio import AioRpcError

from tq42 import exceptions
from functools import wraps

from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def handle_generic_sdk_errors(func: F) -> F:
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except InactiveRpcError as e:
            status_code = e.code()
            if status_code == StatusCode.PERMISSION_DENIED:
                raise exceptions.PermissionDeniedError() from None

            if status_code == StatusCode.UNAUTHENTICATED:
                raise exceptions.UnauthenticatedError() from None

            if status_code in [
                StatusCode.INVALID_ARGUMENT,
                StatusCode.NOT_FOUND,
                StatusCode.UNKNOWN,
            ]:
                # offending command will be second from the last
                # last line is: traceback.extract_stack()
                index = -2 if len(traceback.extract_stack()) > 1 else 0
                raise exceptions.InvalidArgumentError(
                    command=traceback.extract_stack()[index].line, details=e.details()
                ) from None

            raise e
        except AioRpcError:
            raise ConnectionError(
                "Channel disconnected. Please reconnect by re-executing the channel connection."
            ) from None
        except KeyError:
            raise exceptions.NoDefaultError(
                command=traceback.extract_stack()[0].line
            ) from None
        except exceptions.NoMatchingAttributeError as e:
            raise exceptions.InvalidArgumentError(
                command=traceback.extract_stack()[0].line, details=e.details
            )
        except FileExistsError as e:
            raise exceptions.InvalidArgumentError(
                command=traceback.extract_stack()[0].line,
                details=f"File {e} already exists",
            )
        except (
            exceptions.AuthenticationError,
            exceptions.PermissionDeniedError,
            exceptions.UnauthenticatedError,
            exceptions.InvalidArgumentError,
            exceptions.NoDefaultError,
            exceptions.ExceedRetriesError,
            exceptions.LocalPermissionError,
            exceptions.ExperimentRunCancelError,
        ) as e:
            raise e from None
        except (PermissionError, OSError):
            raise exceptions.LocalPermissionError() from None
        except Exception as e:
            # are there generic errors we are not catching here?
            logging.debug(
                "Error {} is raised in SDK and not specifically handled".format(e)
            )
            raise e

    return cast(F, wrapped)
