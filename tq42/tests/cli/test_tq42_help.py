import unittest
from tq42.cli import tq42_help


class MockSubparser:
    def add_parser(
        self,
        name,
        description,
        help,
        formatter_class,
    ):
        return {
            "name": name,
            "description": description,
            "help": help,
            "formatter_class": formatter_class,
        }


class TestTQ42Help(unittest.TestCase):
    def setUp(self):
        self.help_tree = {
            "auth": {
                "help": {"text": "Class to manage authentication", "level": "group"},
                "login": {
                    "help": {
                        "text": "Authenticate with this.",
                        "level": "command",
                        "cli_url": "README.html#authentication",
                        "python_url": "README.html#ptyhon_authentication",
                    }
                },
            },
            "help": {"cli_url": "index.html", "level": "tq42"},
        }

    def tearDown(self):
        pass

    def with_urls_test(self, with_urls):
        self.assertEqual("tq42 org list", with_urls.name)
        self.assertEqual("command", with_urls.level)
        self.assertEqual("test.net/cli/help", with_urls.cli_url)
        self.assertEqual("test.net/python/help", with_urls.python_url)
        self.assertEqual("you need help", with_urls.text)

    def without_urls_test(self, no_urls):
        self.assertEqual("tq42 auth", no_urls.name)
        self.assertEqual("group", no_urls.level)
        self.assertIsNone(no_urls.cli_url)
        self.assertIsNone(no_urls.python_url)
        self.assertEqual("authenticate into tq42", no_urls.text)

    @staticmethod
    def get_help_with_urls():
        return tq42_help.Help(
            name="tq42 org list",
            level="command",
            cli_url="test.net/cli/help",
            python_url="test.net/python/help",
            text="you need help",
        )

    @staticmethod
    def get_help_without_urls():
        return tq42_help.Help(
            name="tq42 auth", level="group", text="authenticate into tq42"
        )

    def test_tq42_help_init(self):
        with_urls = self.get_help_with_urls()
        self.with_urls_test(with_urls)

        no_urls = self.get_help_without_urls()
        self.without_urls_test(no_urls)

    def test_tq42_from_dict(self):
        with_urls = tq42_help.Help.from_dict(
            {
                "name": "tq42 org list",
                "level": "command",
                "cli_url": "test.net/cli/help",
                "python_url": "test.net/python/help",
                "text": "you need help",
            }
        )
        self.with_urls_test(with_urls)

        no_urls = tq42_help.Help.from_dict(
            {"name": "tq42 auth", "level": "group", "text": "authenticate into tq42"}
        )
        self.without_urls_test(no_urls)

    def test_display_text(self):
        with_urls = self.get_help_with_urls()
        expected = "you need help\n\nFor details, see test.net/cli/help"
        actual = with_urls.display_help
        self.assertEqual(expected, actual)

        no_urls = self.get_help_without_urls()
        expected = no_urls.text
        actual = no_urls.display_help
        self.assertEqual(expected, actual)

    def test_display_docstring(self):
        with_urls = self.get_help_with_urls()
        expected = "you need help\n\nFor details, see test.net/python/help"
        actual = with_urls.display_docstring
        self.assertEqual(expected, actual)

        no_urls = self.get_help_without_urls()
        expected = no_urls.text
        actual = no_urls.display_docstring
        self.assertEqual(expected, actual)

    def test_walk_tree_tq42(self):
        expected = {"cli_url": "index.html", "level": "tq42", "name": "tq42"}
        actual = tq42_help.Help.walk_tree([], self.help_tree)
        self.assertEqual(expected, actual)

    def test_walk_tree_tq42_auth(self):
        expected = {
            "text": "Class to manage authentication",
            "level": "group",
            "name": "auth",
        }
        actual = tq42_help.Help.walk_tree(["auth"], self.help_tree)
        self.assertEqual(expected, actual)

    def test_walk_tree_tq42_auth_login(self):
        expected = {
            "text": "Authenticate with this.",
            "level": "command",
            "cli_url": "README.html#authentication",
            "python_url": "README.html#ptyhon_authentication",
            "name": "login",
        }
        actual = tq42_help.Help.walk_tree("auth login".split(), self.help_tree)
        self.assertEqual(expected, actual)

    def test_walk_root(self):
        tree = {
            "help": {
                "cli_url": "https://docs.tq42.com/en/latest/index.html",
                "level": "tq42",
            }
        }
        h = tq42_help.Help.lookup_help([], tree=tree)
        self.assertEqual(h.name, "tq42")

    def test_default_help_tree(self):
        self.assertEqual("tq42", tq42_help.default_help_tree["help"]["level"])
        global_help_object = tq42_help.Help.lookup_help([])
        self.assertEqual("tq42", global_help_object.level)
        self.assertIsNone(global_help_object.text)
        self.assertIsNotNone(global_help_object.cli_url)
        self.assertIsNone(global_help_object.python_url)

    def test_get_global_help(self):
        global_help_object = tq42_help.Help.lookup_help([])
        cli_url = global_help_object.cli_url
        global_help_text = tq42_help.get_commands()
        self.assertEqual(str, type(global_help_text))
        self.assertIn(cli_url, global_help_text)

    def test_add_parser(self):
        subparser = MockSubparser()
        expected = {
            "name": "list",
            "description": "you need help\n\nFor details, see test.net/cli/help",
            "help": "you need help",
        }
        help = self.get_help_with_urls()
        help.name = "list"
        self.assertIsNone(help.argparser)
        actual = help.add_parser(subparser)
        del actual["formatter_class"]
        self.assertEqual(expected, actual)
        self.assertEqual(help.argparser, actual)
