import unittest

from tq42.functional_tests.functional_test_config import FunctionalTestConfig


class TestTestConfig(unittest.TestCase, FunctionalTestConfig):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_functional_test_config(self):
        self.assertIsNotNone(self.org)
        self.assertIsNotNone(self.proj)
        self.assertIsNotNone(self.exp)
        self.assertIsNotNone(self.exp_run)
