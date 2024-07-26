import click

import tq42.cli.utils.cli_functions as cli
from .model_group import model_group
from .dataset_group import dataset_group
from .utils.types import TQ42CliContext


@click.group("proj")
def project_group() -> click.Group:
    """
    Class to manage projects

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Setting_Up_Your_Environment.html#check-your-current-organization-and-project-settings
    """
    pass


@project_group.command("list")
@click.option(
    "--org",
    "org_id",
    required=False,
    type=str,
    help="Attribute the command to a particular organization",
)
@click.pass_context
def list_by_org(ctx: TQ42CliContext, org_id: str) -> None:
    """
    List all the projects you have permission to view within the organization that is currently set.

    e.g.: tq42 proj list --org b0edfd26-0817-4818-a278-17ef6c14e3a5

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Setting_Up_Your_Environment.html#list-all-projects
    """
    click.echo(cli.list_proj_by_org(ctx.obj.client, org_id))


@project_group.command("show")
@click.pass_context
def show_default(ctx: TQ42CliContext) -> None:
    """
    Show the current organization, project ID and associated project friendly name (if any).

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Setting_Up_Your_Environment.html#check-your-current-organization-and-project-settings
    """
    click.echo(cli.proj_show(ctx.obj.client))


@project_group.command("set")
@click.argument("proj_id", required=True, type=str)
@click.pass_context
def set_default(ctx: TQ42CliContext, proj_id: str) -> None:
    """
    Change the active project.

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Setting_Up_Your_Environment.html#changing-your-workspace-to-a-different-organization-or-project
    """
    click.echo(cli.set_project(ctx.obj.client, proj_id=proj_id))


@project_group.command("set-friendly-name")
@click.argument("friendly_name", required=True, type=str)
@click.option(
    "--proj",
    "proj_id",
    required=True,
    type=str,
    help="Attribute the command to a particular project",
)
@click.pass_context
def proj_set_friendly_name(
    ctx: TQ42CliContext, friendly_name: str, proj_id: str
) -> None:
    """
    Set a friendly name for a project.

    tq42 proj set-friendly-name NEW_FRIENDLY_NAME --proj b0edfd26-0817-4818-a278-17ef6c14e3a5

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Setting_Up_Your_Environment.html#setting-friendly-names-for-projects-and-experiments
    """
    click.echo(
        cli.proj_update(ctx.obj.client, proj_id=proj_id, friendly_name=friendly_name)
    )


project_group.add_command(model_group)
project_group.add_command(dataset_group)
