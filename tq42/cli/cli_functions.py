from tq42.cli.output_format.formatter import (
    org_formatter,
    proj_formatter,
    exp_formatter,
    run_formatter,
    set_proj_lines,
)
from tq42.organization import list_all as list_all_organizations, Organization
from tq42.project import list_all as list_all_projects, Project
from tq42.experiment import list_all as list_all_experiments, Experiment
from tq42.experiment_run import list_all as list_all_experiment_runs, ExperimentRun

from tq42.client import TQ42Client


def list_orgs(client: TQ42Client) -> str:
    org_list = org_formatter.format_by_list_object(
        list_all_organizations(client=client)
    )
    result = "\n".join(org_list)
    return result


def proj_update(client: TQ42Client, args) -> str:
    proj = args.proj
    friendly_name = args.name
    updated_proj = Project(client=client, id=proj).update(name=friendly_name)
    result = proj_formatter.format(updated_proj)
    return result


def exp_update(client: TQ42Client, args) -> str:
    exp = args.exp
    result = exp_formatter.format(
        Experiment(client=client, id=exp).update(name=args.name)
    )
    return result


def list_proj_by_org(client: TQ42Client, org: str) -> str:
    project_list = proj_formatter.format_by_list_object(
        list_all_projects(client=client, organization_id=org)
    )
    result = "\n".join(project_list)
    return result


def get_exprun(client: TQ42Client, run_id: str) -> str:
    result = run_formatter.run_checked_lines(
        ExperimentRun(client=client, id=run_id).data
    )
    result = "\n".join(result)
    return result


def list_exp_by_proj(client: TQ42Client, proj: str) -> str:
    result = exp_formatter.format_by_list_object(
        list_all_experiments(client=client, project_id=proj)
    )
    result = "\n".join(result)
    return result


def list_expruns(client: TQ42Client, exp: str) -> str:
    result = run_formatter.format_by_list_object(
        list_all_experiment_runs(client=client, experiment_id=exp)
    )
    result = "\n".join(result)
    return result


def cancel_exprun(client: TQ42Client, run_id: str) -> str:
    # if not cancelled it will raise an Exception
    ExperimentRun(client=client, id=run_id).cancel()
    return "The experiment run is cancelled."


def set_org(client: TQ42Client, org_id: str) -> str:
    Organization(client=client, id=org_id).set()
    project = Project.show(client=client)
    result = set_proj_lines(proj=project)
    return "\n".join(result)


def set_project(client: TQ42Client, proj_id: str) -> str:
    project = Project(client=client, id=proj_id).set()
    result = set_proj_lines(project)
    result = "\n".join(result)
    return result


def proj_show(client: TQ42Client) -> str:
    retrieved = Project.show(client=client)
    result = set_proj_lines(retrieved)
    result = "\n".join(result)
    return result


def poll_exprun(client: TQ42Client, run_id: str) -> str:
    try:
        result = ExperimentRun(client=client, id=run_id).poll()
        result = run_formatter.run_checked_lines(result.data)
        result = "\n".join(result)
        return result

    except Exception as e:
        print(e)
