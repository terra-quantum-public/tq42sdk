from tq42.cli import (
    organization_group as org_group,
    project_group as proj_group,
    experiment_run_group as exp_run_group,
    experiment_group as exp_group,
    compute_group as compute_group,
    project_dataset_group as proj_data_group,
)

from tq42.utils import environment_utils as env_group
from typing import Optional
from tq42.client import TQ42Client


def tq42_all(client: TQ42Client, args) -> Optional[str]:
    if args.group == "auth" and args.command == "login":
        client.login()
    elif args.group == "exp" and args.command == "run":
        return exp_run_group.experiment_run_group(client, args)
    elif args.group == "exp":
        return exp_group.experiment_group(client, args)
    elif args.group == "proj" and args.command == "dataset":
        return proj_data_group.project_dataset_group(client, args)
    elif args.group == "proj":
        return proj_group.project_group(client, args)
    elif args.group == "org":
        return org_group.organization_group(client, args)
    elif args.group == "compute":
        return compute_group.compute_group(args)
    elif args.group == "env":
        return env_group.environment_group(client=client, args=args)
