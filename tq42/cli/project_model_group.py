from tq42.cli.parsers.params_checker import check_params
from tq42.model import Model, list_all


def project_model_group(client, args):
    if args.subcommand == "list":
        return proj_model_list(client, args)

    elif args.subcommand == "get":
        return proj_model_get(client, args)


def proj_model_list(client, args):
    check_params("proj model list", args)
    return [model.data for model in list_all(client=client, project_id=args.proj)]


def proj_model_get(client, args):
    check_params("proj model get", args)
    return Model(client=client, id=args.model).data
