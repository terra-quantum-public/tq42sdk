import click

import tq42.cli.utils.cli_functions as cli
from tq42.cli.utils.types import TQ42CliContext


@click.group("org")
def organization_group() -> click.Group:
    """
    Class to manage organization

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Setting_Up_Your_Environment.html#check-your-current-organization-and-project-settings
    """
    pass


@organization_group.command("list")
@click.pass_context
def list_all(ctx: TQ42CliContext) -> None:
    """
    List all the organizations you have permission to view.

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Setting_Up_Your_Environment.html#list-all-organizations
    """
    res = cli.list_orgs(ctx.obj.client)
    click.echo(res)


@organization_group.command("set")
@click.argument("org_id", required=True)
@click.pass_context
def org_set(ctx: TQ42CliContext, org_id: str) -> None:
    """
    Change the active organization.

    e.g.: tq42 org set 5bac0b60-48d0-45cd-bf0a-39505b058106

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Setting_Up_Your_Environment.html#changing-your-workspace-to-a-different-organization-or-project
    """
    res = cli.set_org(ctx.obj.client, org_id)
    click.echo(res)
