import unittest

from tq42.cli import (
    experiment_group,
    experiment_run_group,
    organization_group,
    project_group,
)
from tq42 import organization
import tq42.cli.utils.formatter as formatter
from tq42.utils import dirs, misc
from tq42.client import TQ42Client


class TestImports(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tq42_imports(self):
        self.assertIsNotNone(organization)

    def test_utils_imports(self):
        self.assertIsNotNone(TQ42Client)
        self.assertIsNotNone(dirs)
        self.assertIsNotNone(misc)

    def test_cli_imports(self):
        self.assertIsNotNone(experiment_group)
        self.assertIsNotNone(experiment_run_group)
        self.assertIsNotNone(organization_group)
        self.assertIsNotNone(project_group)

    def test_formatter_imports(self):
        self.assertIsNotNone(formatter)
