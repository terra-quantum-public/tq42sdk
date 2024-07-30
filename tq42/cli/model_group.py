import click

from tq42.cli.utils.types import TQ42CliContext
from tq42.model import Model, list_all


@click.group("model")
def model_group() -> click.Group:
    """
    Group to manage models.

    https://docs.tq42.com/en/latest/Python_Developer_Guide/Working_with_Models.html
    """
    pass


@model_group.command("list")
@click.option(
    "--proj",
    "proj_id",
    required=True,
    type=str,
    help="Attribute the command to a particular project",
)
@click.pass_context
def list_models(ctx: TQ42CliContext, proj_id: str) -> None:
    """
    List all models within a project.

    e.g.: tq42 proj model list --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Working_with_Models.html
    """
    click.echo(
        [model.data for model in list_all(client=ctx.obj.client, project_id=proj_id)]
    )


@model_group.command("get")
@click.argument("model_id", required=True, type=str)
@click.pass_context
def get(ctx: TQ42CliContext, model_id: str) -> None:
    """
    Get a specific model.

    e.g.: tq42 proj model get 98ccb1d2-a3d0-48c8-b172-022f6db9be01

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Working_with_Models.html
    """
    click.echo(Model(client=ctx.obj.client, id=model_id).data)
