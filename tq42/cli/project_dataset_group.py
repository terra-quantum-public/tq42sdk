from tq42.cli.parsers.params_checker import check_params
from tq42.dataset import Dataset, list_all


def project_dataset_group(client, args):
    if args.subcommand == "create":
        return proj_dataset_create(client, args)

    elif args.subcommand == "list":
        return proj_dataset_list(client, args)

    elif args.subcommand == "get":
        return proj_dataset_get(client, args)

    elif args.subcommand == "export":
        return proj_dataset_export(client, args)


def proj_dataset_list(client, args):
    check_params("proj dataset list", args)
    return [dataset.data for dataset in list_all(client=client, project_id=args.proj)]


def proj_dataset_create(client, args):
    check_params("proj dataset create", args)
    return Dataset.create(
        client=client,
        project_id=args.proj,
        name=args.name,
        description=args.desc,
        url=args.url,
        sensitivity=args.sensitivity.upper(),
    ).data


def proj_dataset_get(client, args):
    check_params("proj dataset get", args)
    return Dataset(client=client, id=args.dataset).data


def proj_dataset_export(client, args):
    check_params("proj dataset export", args)
    dataset = Dataset(client=client, id=args.dataset)
    dataset.export(directory_path=args.directory_path)
