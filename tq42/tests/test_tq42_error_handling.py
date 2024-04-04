import unittest

from grpc import StatusCode
from grpc._channel import _InactiveRpcError as InactiveRpcError, _RPCState as RPCState

from tq42.exceptions import (
    NoDefaultError,
    InvalidArgumentError,
    PermissionDeniedError,
    UnauthenticatedError,
    ExceedRetriesError,
    LocalPermissionError,
)
from tq42.exception_handling import handle_generic_sdk_errors
from tq42.utils.file_handling import read_file
from tq42.utils.constants import (
    no_default_error_file,
    unauthenticated_error_file,
    insufficient_permission_errors_file,
    invalid_arguments_error_file,
    local_permission_error_file,
)


class TestTq42ErrorHandling(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def fail_if_still_here(self):
        self.assertTrue(False)

    def test_decorator_happy_path(self):
        @handle_generic_sdk_errors
        def happy_path():
            return "happy"

        self.assertEqual(happy_path(), "happy")

    def test_decorator_happy_path_with_params(self):
        @handle_generic_sdk_errors
        def summarize(a: int, b: int, c: int, d: int, e: int) -> int:
            return a + b + c + d + e

        self.assertEqual(summarize(1, 2, 3, 4, 5), 15)

    def test_decorator_invalid_argument_error(self):
        @handle_generic_sdk_errors
        def raise_invalid_argument():
            raise InvalidArgumentError("command", "details")

        try:
            raise_invalid_argument()
            self.fail_if_still_here()
        except InvalidArgumentError as e:
            self.assertEqual(
                str(e),
                read_file(invalid_arguments_error_file).format(e.command, e.details),
            )

    def test_decorator_grpc_invalid_argument_error(self):
        @handle_generic_sdk_errors
        def raise_invalid_argument_grpc():
            raise InactiveRpcError(
                RPCState(
                    code=StatusCode.INVALID_ARGUMENT,
                    details="no details",
                    due=[],
                    initial_metadata=[],
                    trailing_metadata=[],
                )
            )

        try:
            raise_invalid_argument_grpc()
            self.fail_if_still_here()
        except InvalidArgumentError as e:
            self.assertEqual(
                str(e),
                read_file(invalid_arguments_error_file).format(e.command, e.details),
            )

    def test_decorator_grpc_status_not_found_error(self):
        @handle_generic_sdk_errors
        def raise_status_not_found_grpc():
            raise InactiveRpcError(
                RPCState(
                    code=StatusCode.NOT_FOUND,
                    details="no details",
                    due=[],
                    initial_metadata=[],
                    trailing_metadata=[],
                )
            )

        try:
            raise_status_not_found_grpc()
            self.fail_if_still_here()
        except InvalidArgumentError as e:
            self.assertEqual(
                str(e),
                read_file(invalid_arguments_error_file).format(e.command, e.details),
            )

    def test_decorator_permission_denied_error(self):
        @handle_generic_sdk_errors
        def raise_permission_denied():
            raise PermissionDeniedError()

        try:
            raise_permission_denied()
            self.fail_if_still_here()
        except PermissionDeniedError as e:
            self.assertEqual(str(e), read_file(insufficient_permission_errors_file))

    def test_decorator_grpc_permission_denied_error(self):
        @handle_generic_sdk_errors
        def raise_permission_denied_grpc():
            raise InactiveRpcError(
                RPCState(
                    code=StatusCode.PERMISSION_DENIED,
                    details="no details",
                    due=[],
                    initial_metadata=[],
                    trailing_metadata=[],
                )
            )

        try:
            raise_permission_denied_grpc()
            self.fail_if_still_here()
        except PermissionDeniedError as e:
            self.assertEqual(str(e), read_file(insufficient_permission_errors_file))

    def test_decorator_unauthenticated_error(self):
        @handle_generic_sdk_errors
        def raise_unauthenticated():
            raise UnauthenticatedError()

        try:
            raise_unauthenticated()
            self.fail_if_still_here()
        except UnauthenticatedError as e:
            self.assertEqual(str(e), read_file(unauthenticated_error_file))

    def test_decorator_grpc_unauthenticated_error(self):
        @handle_generic_sdk_errors
        def raise_unauthenticated_grpc():
            raise InactiveRpcError(
                RPCState(
                    code=StatusCode.UNAUTHENTICATED,
                    details="no details",
                    due=[],
                    initial_metadata=[],
                    trailing_metadata=[],
                )
            )

        try:
            raise_unauthenticated_grpc()
            self.fail_if_still_here()
        except UnauthenticatedError as e:
            self.assertEqual(str(e), read_file(unauthenticated_error_file))

    def test_decorator_no_default_error(self):
        @handle_generic_sdk_errors
        def raise_no_default():
            raise NoDefaultError("command")

        try:
            raise_no_default()
            self.fail_if_still_here()
        except NoDefaultError as e:
            self.assertEqual(str(e), read_file(no_default_error_file).format(e.command))

    def test_decorator_key_error(self):
        @handle_generic_sdk_errors
        def raise_key_error():
            raise KeyError()

        try:
            raise_key_error()
            self.fail_if_still_here()
        except NoDefaultError as e:
            self.assertEqual(str(e), read_file(no_default_error_file).format(e.command))

    def test_decorator_exceed_retries_error(self):
        @handle_generic_sdk_errors
        def raise_exceed_retries():
            raise ExceedRetriesError(5)

        try:
            raise_exceed_retries()
            self.fail_if_still_here()
        except ExceedRetriesError as e:
            self.assertEqual(str(e), "Polling exceeded. Number of retries: 5")

    def test_decorator_local_permission_error(self):
        @handle_generic_sdk_errors
        def raise_local_permission_error():
            raise LocalPermissionError()

        try:
            raise_local_permission_error()
            self.fail_if_still_here()
        except LocalPermissionError as e:
            self.assertEqual(str(e), read_file(local_permission_error_file))

    def test_decorator_permission_error(self):
        @handle_generic_sdk_errors
        def raise_permission_error():
            raise PermissionError()

        try:
            raise_permission_error()
            self.fail_if_still_here()
        except LocalPermissionError as e:
            self.assertEqual(str(e), read_file(local_permission_error_file))

    def test_decorator_os_error(self):
        @handle_generic_sdk_errors
        def raise_os_error():
            raise OSError()

        try:
            raise_os_error()
            self.fail_if_still_here()
        except LocalPermissionError as e:
            self.assertEqual(str(e), read_file(local_permission_error_file))

    def test_generic_error(self):
        @handle_generic_sdk_errors
        def raise_generic_error():
            raise Exception("generic exception")

        self.assertRaises(Exception, raise_generic_error)
