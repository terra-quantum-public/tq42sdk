import unittest

from tq42 import __main__ as main
from tq42.cli import (
    cli_functions,
    compute_group,
    experiment_group,
    experiment_run_group,
    organization_group,
    project_group,
    tq42_all,
    tq42_help,
)
from tq42 import algorithm, organization
from tq42.cli.output_format import formatter
from tq42.cli.parsers import params_checker, tq42parser
from tq42.utils import dirs, utils
from tq42.client import TQ42Client


class TestImports(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        self.assertIsNotNone(main)

    def test_tq42_imports(self):
        self.assertIsNotNone(algorithm)
        self.assertIsNotNone(organization)

    def test_utils_imports(self):
        self.assertIsNotNone(TQ42Client)
        self.assertIsNotNone(dirs)
        self.assertIsNotNone(utils)

    def test_cli_imports(self):
        self.assertIsNotNone(cli_functions)
        self.assertIsNotNone(compute_group)
        self.assertIsNotNone(experiment_group)
        self.assertIsNotNone(experiment_run_group)
        self.assertIsNotNone(organization_group)
        self.assertIsNotNone(project_group)
        self.assertIsNotNone(tq42_all)
        self.assertIsNotNone(tq42_help)

    def test_parser_imports(self):
        self.assertIsNotNone(params_checker)
        self.assertIsNotNone(tq42parser)

    def test_formatter_imports(self):
        self.assertIsNotNone(formatter)
