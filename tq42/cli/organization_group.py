import tq42.cli.cli_functions as cli
from tq42.cli.parsers.params_checker import check_params


def organization_group(client, args):
    res = None
    if args.command == "set":
        res = org_set(client, args)

    elif args.command == "list":
        res = cli.list_orgs(client)

    return res


def org_set(client, args):
    check_params("org set", args)
    res = cli.set_org(client, args.org)

    return res
