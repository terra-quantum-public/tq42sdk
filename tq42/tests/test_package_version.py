import unittest

import tq42


class TestPackageVersion(unittest.TestCase):
    def test_package_version(self):
        self.assertIsNotNone(tq42.__version__)
