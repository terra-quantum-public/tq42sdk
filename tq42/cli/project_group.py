import tq42.cli.cli_functions as cli


def project_group(client, args):
    res = None
    if args.command == "list":
        res = cli.list_proj_by_org(client, args.org)
    elif args.command == "show":
        res = cli.proj_show(client)
    elif args.command == "set":
        res = cli.set_project(client, args.proj)
    elif args.command == "set-friendly-name":
        res = proj_set_friendly_name(client, args)

    return res


def proj_set_friendly_name(client, args):
    if args.name is None or args.proj is None:
        example_command = 'Example usage: tq42 proj set-friendly-name "FRIENDLY_NAME" --proj="PROJ_ID"\n'
        print(example_command)
        return

    return cli.proj_update(client, args)
