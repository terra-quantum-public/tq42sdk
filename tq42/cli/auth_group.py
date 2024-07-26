import click

from tq42.cli.utils.types import TQ42CliContext


@click.group("auth")
def auth_group() -> click.Group:
    pass


@auth_group.command("login")
@click.pass_context
def login(ctx: TQ42CliContext) -> None:
    ctx.obj.client.login()
