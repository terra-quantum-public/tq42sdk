import click

import tq42.cli.utils.cli_functions as cli
import tq42.utils.cache as cache_utils
from .experiment_run_group import exp_run_group
from .utils.types import TQ42CliContext


@click.group("exp")
def experiment_group() -> click.Group:
    pass


@experiment_group.command(
    "list", help="e.g.: tq42 exp list --proj b0edfd26-0817-4818-a278-17ef6c14e3a5"
)
@click.option(
    "--proj",
    "proj_id",
    required=False,
    type=str,
    help="Attribute the command to a particular project",
)
@click.pass_context
def list_by_proj(ctx: TQ42CliContext, proj_id: str) -> None:
    # TODO: Need to display error message to stderr when no proj is specified or set.
    #  Should do this by raising an exception and displaying from main function

    error_msg = "No project id is set. \nExample: tq42 exp list --proj b0edfd26-0817-4818-a278-17ef6c14e3a5"

    if proj_id is None:
        proj = cache_utils.get_current_value("proj")
        if proj == "":
            click.echo(error_msg)
            return

    click.echo(cli.list_exp_by_proj(ctx.obj.client, proj_id))


@experiment_group.command(
    "set-friendly-name",
    help="e.g.: tq42 exp set-friendly-name NEW_FRIENDLY_NAME --exp b0edfd26-0817-4818-a278-17ef6c14e3a5",
)
@click.argument("friendly_name", required=True, type=str)
@click.option(
    "--exp",
    "exp_id",
    required=True,
    type=str,
    help="Attribute the command to a particular experiment",
)
@click.pass_context
def set_friendly_name(ctx: TQ42CliContext, friendly_name: str, exp_id: str) -> None:
    click.echo(cli.exp_update(ctx.obj.client, exp_id=exp_id, name=friendly_name))


experiment_group.add_command(exp_run_group)
