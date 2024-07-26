import click

from tq42.cli.utils.types import TQ42CliContext
from tq42.model import Model, list_all


@click.group("model", help="Command group to manage models")
def model_group() -> click.Group:
    pass


@model_group.command(
    "list",
    help="e.g.: tq42 proj model list --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01",
)
@click.option("--proj", "proj_id", required=True, type=str)
@click.pass_context
def list_models(ctx: TQ42CliContext, proj_id: str) -> None:
    click.echo(
        [model.data for model in list_all(client=ctx.obj.client, project_id=proj_id)]
    )


@model_group.command(
    "get", help="e.g.: tq42 proj model get 98ccb1d2-a3d0-48c8-b172-022f6db9be01"
)
@click.argument("model_id", required=True, type=str)
@click.pass_context
def get(ctx: TQ42CliContext, model_id: str) -> None:
    click.echo(Model(client=ctx.obj.client, id=model_id).data)
