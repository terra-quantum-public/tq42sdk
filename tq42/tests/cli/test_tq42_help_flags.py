import unittest
from tq42.cli import tq42_help


class MockParser:
    result = None

    def add_argument(self, first_flag, second_flag=None, help=None, metavar=None):
        if second_flag is not None:
            short_flag = first_flag
            flag = second_flag
        else:
            short_flag = None
            flag = first_flag
        self.result = {
            "flag": flag,
            "short_flag": short_flag,
            "help": help,
            "metavar": metavar,
        }


class TestTQ42HelpFlags(unittest.TestCase):
    def setUp(self):
        self.org_flag = {
            "metavar": "ORG_ID",
            "text": "Attribute the command to a particular organization",
            "flag": "--org",
        }
        self.visibility_flag = {
            "text": "Specify the visibility of an attribute",
            "flag": "--visibility",
        }
        self.version_flag = {
            "text": "Display version number",
            "flag": "--version",
            "short_flag": "-V",
        }
        self.help_list = [self.org_flag, self.visibility_flag, self.version_flag]

    def tearDown(self):
        pass

    def test_default_flags(self):
        d = tq42_help.default_help_flags
        self.assertIn("org", d)
        h = d["org"]
        self.assertEqual("--org", h.flag)
        self.assertIsNone(h.short_flag)
        self.assertEqual("Attribute the command to a particular organization", h.text)
        self.assertEqual("ORG_ID", h.metavar)

    def test_from_dict_with_metavar(self):
        h = tq42_help.HelpFlag.from_dict(self.org_flag)
        self.assertEqual("ORG_ID", h.metavar)
        self.assertEqual("Attribute the command to a particular organization", h.text)
        self.assertEqual("--org", h.flag)
        self.assertIsNone(h.short_flag)

    def test_from_dict_without_metavar(self):
        h = tq42_help.HelpFlag.from_dict(self.visibility_flag)
        self.assertIsNone(h.metavar)
        self.assertEqual("Specify the visibility of an attribute", h.text)
        self.assertEqual("--visibility", h.flag)
        self.assertIsNone(h.short_flag)

    def test_from_dict_with_short_flag(self):
        h = tq42_help.HelpFlag.from_dict(self.version_flag)
        self.assertIsNone(h.metavar)
        self.assertEqual("Display version number", h.text)
        self.assertEqual("--version", h.flag)
        self.assertEqual("-V", h.short_flag)

    def test_flag_list_to_dict(self):
        d = tq42_help.HelpFlag.flag_list_to_dict(self.help_list)
        expected = ["org", "version", "visibility"]
        actual = list(d.keys())
        actual.sort()
        self.assertEqual(expected, actual)

    def test_add_flag(self):
        parser = MockParser()

        h = tq42_help.HelpFlag.from_dict(self.org_flag)
        h.add_argument(parser)
        actual = parser.result
        expected = {
            "flag": "--org",
            "short_flag": None,
            "help": "Attribute the command to a particular organization",
            "metavar": "ORG_ID",
        }
        self.assertEqual(expected, actual)

        h = tq42_help.HelpFlag.from_dict(self.visibility_flag)
        h.add_argument(parser)
        actual = parser.result
        expected = {
            "flag": "--visibility",
            "short_flag": None,
            "help": "Specify the visibility of an attribute",
            "metavar": None,
        }
        self.assertEqual(expected, actual)

        h = tq42_help.HelpFlag.from_dict(self.version_flag)
        h.add_argument(parser)
        actual = parser.result
        expected = {
            "flag": "--version",
            "short_flag": "-V",
            "help": "Display version number",
            "metavar": None,
        }
        self.assertEqual(expected, actual)
