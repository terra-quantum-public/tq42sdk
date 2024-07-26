import click

from tq42.cli.utils.types import TQ42CliContext
from tq42.utils.environment import (
    get_environment,
    environment_default_set,
    environment_clear,
)


@click.group("env")
def environment_group() -> click.Group:
    pass


@environment_group.command("print")
def print_environment():
    click.echo(get_environment())


@environment_group.command("default")
@click.pass_context
def default_environment(ctx: TQ42CliContext):
    click.echo(environment_default_set(client=ctx.obj.client))


@environment_group.command("clear")
def clear_environment():
    click.echo(environment_clear())
