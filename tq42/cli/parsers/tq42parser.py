import argparse
import textwrap

import tq42
from tq42.cli import tq42_help


def parse_args(args):
    if len(args) < 1:
        args = ["--help"]
    parser = argparse.ArgumentParser(
        prog="tq42",
        description=textwrap.dedent(tq42_help.get_commands()),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    config_flag = tq42_help.default_help_flags["config"]
    config_flag.add_argument(parser)

    version_flag = tq42_help.default_help_flags["version"]
    parser.add_argument(
        version_flag.short_flag,
        version_flag.flag,
        help=version_flag.text,
        action="version",
        version=tq42.__version__,
    )

    group_parser = parser.add_subparsers(dest="group")

    add_auth_parser(group_parser)
    add_compute_parser(group_parser)
    add_proj_parser(group_parser)
    add_exp_parser(group_parser)

    add_org_parser(group_parser)
    add_env_parser(group_parser)

    args = parser.parse_args(args)
    return args


def add_auth_parser(group_parser):
    auth_help = tq42_help.Help.lookup_help(["auth"])
    auth_parser = auth_help.add_parser(group_parser)

    auth_subparser = auth_parser.add_subparsers(dest="command")

    login_help = tq42_help.Help.lookup_help("auth login".split())
    login_help.add_parser(auth_subparser)


def add_proj_parser(group_parser):
    proj_help = tq42_help.Help.lookup_help(["proj"])
    proj_parser = proj_help.add_parser(group_parser)

    proj_subparser = proj_parser.add_subparsers(dest="command")

    list_help = tq42_help.Help.lookup_help("proj list".split())
    list_help.add_parser(proj_subparser)
    list_help.add_flag("org")

    show_help = tq42_help.Help.lookup_help("proj show".split())
    show_help.add_parser(proj_subparser)

    set_help = tq42_help.Help.lookup_help("proj set".split())
    proj_set_parser = set_help.add_parser(proj_subparser)
    proj_set_parser.add_argument("proj")

    friendlyname_help = tq42_help.Help.lookup_help("proj set-friendly-name".split())
    proj_friendlyname_parser = friendlyname_help.add_parser(proj_subparser)
    proj_friendlyname_parser.add_argument("name", nargs="?")
    friendlyname_help.add_flag("proj")

    add_proj_dataset_parser(proj_subparser)


def add_proj_dataset_parser(proj_subparser):
    run_help = tq42_help.Help.lookup_help("proj dataset".split())
    proj_subparser = run_help.add_parser(proj_subparser)
    cmd_parser = proj_subparser.add_subparsers(dest="subcommand")

    create_help = tq42_help.Help.lookup_help("proj dataset create".split())
    create_help.add_parser(cmd_parser)
    create_help.add_flag("proj")
    create_help.add_flag("name")
    create_help.add_flag("desc")
    create_help.add_flag("url")
    create_help.add_flag("sensitivity")

    list_help = tq42_help.Help.lookup_help("proj dataset list".split())
    list_help.add_parser(cmd_parser)
    list_help.add_flag("proj")

    get_help = tq42_help.Help.lookup_help("proj dataset get".split())
    dataset_get_parser = get_help.add_parser(cmd_parser)
    dataset_get_parser.add_argument("dataset")

    export_help = tq42_help.Help.lookup_help("proj dataset export".split())
    dataset_export_parser = export_help.add_parser(cmd_parser)
    dataset_export_parser.add_argument("dataset")
    dataset_export_parser.add_argument("directory_path")


def add_org_parser(group_parser):
    org_help = tq42_help.Help.lookup_help(["org"])
    org_parser = org_help.add_parser(group_parser)

    auth_subparser = org_parser.add_subparsers(dest="command")

    set_help = tq42_help.Help.lookup_help("org set".split())
    org_set_parser = set_help.add_parser(auth_subparser)
    org_set_parser.add_argument("org", nargs="?")

    list_help = tq42_help.Help.lookup_help("org list".split())
    list_help.add_parser(auth_subparser)


def add_exp_parser(group_parser):
    exp_help = tq42_help.Help.lookup_help(["exp"])
    exp_parser = exp_help.add_parser(group_parser)

    exp_subparser = exp_parser.add_subparsers(dest="command")

    # tq42 exp list --proj
    list_help = tq42_help.Help.lookup_help("exp list".split())
    list_help.add_parser(exp_subparser)
    list_help.add_flag("proj")

    friendlyname_help = tq42_help.Help.lookup_help("exp set-friendly-name".split())
    exp_setfriendlyname_parser = friendlyname_help.add_parser(exp_subparser)
    exp_setfriendlyname_parser.add_argument("name")
    friendlyname_help.add_flag("exp")

    # tq42 exp run commands
    add_exp_run_parser(exp_subparser)


def add_exp_run_parser(exp_parser):
    run_help = tq42_help.Help.lookup_help("exp run".split())
    exp_parser = run_help.add_parser(exp_parser)

    cmd_parser = exp_parser.add_subparsers(dest="subcommand")

    create_help = tq42_help.Help.lookup_help("exp run create".split())
    create_help.add_parser(cmd_parser)
    create_help.add_flag("exp")
    create_help.add_flag("compute")
    create_help.add_flag("algorithm")
    create_help.add_flag("parameters")

    check_help = tq42_help.Help.lookup_help("exp run check".split())
    check_parser = check_help.add_parser(cmd_parser)
    check_parser.add_argument("run")

    cancel_help = tq42_help.Help.lookup_help("exp run cancel".split())
    cancel_parser = cancel_help.add_parser(cmd_parser)
    cancel_parser.add_argument("run")

    list_help = tq42_help.Help.lookup_help("exp run list".split())
    list_help.add_parser(cmd_parser)
    list_help.add_flag("exp")

    poll_help = tq42_help.Help.lookup_help("exp run poll".split())
    poll_parser = poll_help.add_parser(cmd_parser)
    poll_parser.add_argument("run")


def add_compute_parser(group_parser):
    compute_help = tq42_help.Help.lookup_help(["compute"])
    compute_parser = compute_help.add_parser(group_parser)

    compute_subparser = compute_parser.add_subparsers(dest="command")

    list_help = tq42_help.Help.lookup_help("compute list".split())
    list_help.add_parser(compute_subparser)

    details_help = tq42_help.Help.lookup_help("compute show-details".split())
    details_help.add_parser(compute_subparser)
    details_help.add_flag("compute")


def add_env_parser(group_parser):
    env_parser = group_parser.add_parser("env")

    env_subparser = env_parser.add_subparsers(dest="command")
    env_subparser.add_parser("default")

    env_subparser.add_parser("print")
    env_subparser.add_parser("clear")
