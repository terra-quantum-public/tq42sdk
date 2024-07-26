import click

import tq42.cli.utils.cli_functions as cli
from tq42.cli.utils.types import TQ42CliContext


@click.group("org")
def organization_group() -> click.Group:
    pass


@organization_group.command("list")
@click.pass_context
def list_all(ctx: TQ42CliContext) -> None:
    res = cli.list_orgs(ctx.obj.client)
    click.echo(res)


@organization_group.command(
    "set", help="e.g.: tq42 org set 5bac0b60-48d0-45cd-bf0a-39505b058106"
)
@click.argument("org_id", required=True)
@click.pass_context
def org_set(ctx: TQ42CliContext, org_id: str) -> None:
    res = cli.set_org(ctx.obj.client, org_id)
    click.echo(res)
