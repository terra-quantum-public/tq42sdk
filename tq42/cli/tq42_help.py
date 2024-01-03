import textwrap
import json
from argparse import RawTextHelpFormatter

from tq42.utils import dirs


class Help:
    def __init__(self, name, level, text=None, cli_url=None, python_url=None):
        self.name = name
        self.level = level
        self.cli_url = cli_url
        self.python_url = python_url
        self.text = text
        self.argparser = None

    def add_parser(self, subparser):
        self.argparser = subparser.add_parser(
            self.name,
            description=self.display_help,
            help=self.text,
            formatter_class=RawTextHelpFormatter,
        )
        return self.argparser

    def add_flag(self, flag, help_flags=None):
        if help_flags is None:
            help_flags = default_help_flags

        help_flag = help_flags[flag]
        help_flag.add_argument(self.argparser)

    @property
    def display_help(self):
        text = self.text
        if self.cli_url is not None:
            text = f"{textwrap.dedent(text)}\n\nFor details, see {self.cli_url}"
        return text

    @property
    def display_docstring(self):
        text = self.text
        if self.python_url is not None:
            text = f"{textwrap.dedent(text)}\n\nFor details, see {self.python_url}"
        return text

    @staticmethod
    def from_dict(d: dict):
        return Help(
            name=d["name"],
            level=d["level"],
            text=d.get("text", None),
            cli_url=d.get("cli_url", None),
            python_url=d.get("python_url", None),
        )

    @staticmethod
    def walk_tree(nodes, tree: dict = None):
        if tree is None:
            tree = default_help_tree
        d = tree
        for node in nodes:
            d = d[node]
        d = d["help"].copy()
        if len(nodes) > 0:
            name = nodes[-1]
        else:
            name = "tq42"
        d["name"] = name
        return d

    @staticmethod
    def lookup_help(nodes, tree: dict = None):
        d = Help.walk_tree(nodes, tree)
        return Help.from_dict(d)


def get_help_tree():
    with open(dirs.text_files_dir("help.json")) as f:
        return json.load(f)


default_help_tree = get_help_tree()


def get_commands():
    global_help_object = Help.lookup_help([])
    cli_url = global_help_object.cli_url
    tq42_commands_file_path = dirs.full_path(dirs.text_files_dir(), "tq42_commands.txt")
    with open(tq42_commands_file_path, "r") as f:
        return str(f.read()).format(cli_url)


class HelpFlag:
    def __init__(self, flag, text, metavar=None, short_flag=None):
        self.flag = flag
        self.text = text
        self.metavar = metavar
        self.short_flag = short_flag

    @staticmethod
    def from_dict(d: dict):
        return HelpFlag(
            flag=d["flag"],
            text=d["text"],
            metavar=d.get("metavar", None),
            short_flag=d.get("short_flag", None),
        )

    @staticmethod
    def flag_list_to_dict(a):
        return {d["flag"].replace("--", ""): HelpFlag.from_dict(d) for d in a}

    def add_argument(self, parser):
        if self.short_flag is None:
            parser.add_argument(self.flag, help=self.text, metavar=self.metavar)
        else:
            parser.add_argument(
                self.short_flag, self.flag, help=self.text, metavar=self.metavar
            )


def get_flags():
    with open(dirs.text_files_dir("help_flags.json")) as f:
        return HelpFlag.flag_list_to_dict(json.load(f))


default_help_flags = get_flags()
