import unittest

from tq42.functional_tests.functional_test_config import FunctionalCLITestConfig


class TestFunctionalInvokeCliComputeGroup(unittest.TestCase, FunctionalCLITestConfig):
    def test_compute_list(self):
        result = self.runner.invoke(self.cli_entry, ["compute", "list"])
        assert result.exit_code == 0
        assert result.output is not None

    def test_show_details_should_throw_error_if_no_compute_config(self):
        result = self.runner.invoke(self.cli_entry, ["compute", "show-details"])
        assert result.exit_code == 2

    def test_compute_show_details_small(self):
        result = self.runner.invoke(
            self.cli_entry, ["compute", "show-details", "--compute=SMALL"]
        )
        assert result.exit_code == 0
        assert result.output is not None

    def test_compute_show_details_small_gpu(self):
        result = self.runner.invoke(
            self.cli_entry, ["compute", "show-details", "--compute=SMALL_GPU"]
        )
        assert result.exit_code == 0
        assert result.output is not None

    def test_compute_show_details_large(self):
        result = self.runner.invoke(
            self.cli_entry, ["compute", "show-details", "--compute=LARGE"]
        )
        assert result.exit_code == 0
        assert result.output is not None

    def test_compute_show_details_large_gpu(self):
        result = self.runner.invoke(
            self.cli_entry, ["compute", "show-details", "--compute=LARGE_GPU"]
        )
        assert result.exit_code == 0
        assert result.output is not None
