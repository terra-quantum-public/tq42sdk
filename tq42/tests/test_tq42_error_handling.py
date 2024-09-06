import unittest

from grpc import StatusCode
from grpc._channel import _InactiveRpcError as InactiveRpcError, _RPCState as RPCState

from tq42.exceptions import (
    NoDefaultError,
    InvalidArgumentError,
    PermissionDeniedError,
    UnauthenticatedError,
    ExceedRetriesError,
)
from tq42.utils.exception_handling import handle_generic_sdk_errors


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

        with self.assertRaises(InvalidArgumentError) as cm:
            raise_invalid_argument()
            self.assertEqual(cm.exception.details, "no details")
            self.assertEqual(cm.exception.command, "command")

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

        with self.assertRaises(InvalidArgumentError) as cm:
            raise_invalid_argument_grpc()
            self.assertEqual(cm.exception.details, "no details")
            self.assertIsNotNone(cm.exception.command)

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

        with self.assertRaises(InvalidArgumentError) as cm:
            raise_status_not_found_grpc()
            self.assertEqual(cm.exception.details, "no details")
            self.assertIsNotNone(cm.exception.command)

    def test_decorator_permission_denied_error(self):
        @handle_generic_sdk_errors
        def raise_permission_denied():
            raise PermissionDeniedError()

        with self.assertRaises(PermissionDeniedError):
            raise_permission_denied()

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

        with self.assertRaises(PermissionDeniedError):
            raise_permission_denied_grpc()

    def test_decorator_unauthenticated_error(self):
        @handle_generic_sdk_errors
        def raise_unauthenticated():
            raise UnauthenticatedError()

        with self.assertRaises(UnauthenticatedError):
            raise_unauthenticated()

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

        with self.assertRaises(UnauthenticatedError):
            raise_unauthenticated_grpc()

    def test_decorator_no_default_error(self):
        @handle_generic_sdk_errors
        def raise_no_default():
            raise NoDefaultError("command")

        with self.assertRaises(NoDefaultError) as cm:
            raise_no_default()
            self.assertEqual(cm.exception.command, "command")

    def test_decorator_key_error(self):
        @handle_generic_sdk_errors
        def raise_key_error():
            raise KeyError()

        with self.assertRaises(NoDefaultError) as cm:
            raise_key_error()
            self.assertEqual(
                cm.exception.command,
                "sys.exit(pytest.main(args, plugins_to_load + [Plugin]))",
            )

    def test_decorator_exceed_retries_error(self):
        @handle_generic_sdk_errors
        def raise_exceed_retries():
            raise ExceedRetriesError(5)

        with self.assertRaises(ExceedRetriesError) as cm:
            raise_exceed_retries()
            self.assertEqual(cm.exception.tries, 5)

    def test_generic_error(self):
        @handle_generic_sdk_errors
        def raise_generic_error():
            raise Exception("generic exception")

        with self.assertRaises(Exception):
            raise_generic_error()
