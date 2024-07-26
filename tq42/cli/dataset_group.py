import click

from tq42.cli.utils.types import TQ42CliContext
from tq42.dataset import Dataset, list_all, DatasetSensitivityProto


@click.group("dataset", help="Command group to manage datasets")
def dataset_group() -> click.Group:
    pass


@dataset_group.command(
    "create",
    help='e.g.: tq42 proj dataset create --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01 --name "Example Dataset Name" --desc "Example Description"  --url "https://mydata.com/drive/my-drive" --sensitivity "confidential"',
)
@click.option("--proj", "proj_id", required=True, type=str)
@click.option("--name", "name", required=True, type=str)
@click.option("--desc", "description", required=True, type=str)
@click.option("--url", "url", required=True, type=str)
@click.option("--sensitivity", "sensitivity", required=True, type=str)
@click.pass_context
def create_dataset(
    ctx: TQ42CliContext,
    proj_id: str,
    name: str,
    description: str,
    url: str,
    sensitivity: str,
) -> None:
    click.echo(
        Dataset.create(
            client=ctx.obj.client,
            project_id=proj_id,
            name=name,
            description=description,
            url=url,
            sensitivity=DatasetSensitivityProto.Value(sensitivity.upper()),
        ).data
    )


@dataset_group.command(
    "list",
    help="e.g.: tq42 proj dataset list --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01",
)
@click.option("--proj", "proj_id", required=True, type=str)
@click.pass_context
def list_datasets(ctx: TQ42CliContext, proj_id: str) -> None:
    click.echo(
        [
            dataset.data
            for dataset in list_all(client=ctx.obj.client, project_id=proj_id)
        ]
    )


@dataset_group.command(
    "get", help="e.g.: tq42 proj dataset get 98ccb1d2-a3d0-48c8-b172-022f6db9be01"
)
@click.argument("dataset_id", required=True, type=str)
@click.pass_context
def get(ctx: TQ42CliContext, dataset_id: str) -> None:
    click.echo(Dataset(client=ctx.obj.client, id=dataset_id).data)


@dataset_group.command(
    "export",
    help="e.g.: tq42 proj dataset export 98ccb1d2-a3d0-48c8-b172-022f6db9be01 /Users/user1/Downloads",
)
@click.argument("dataset_id", required=True, type=str)
@click.argument("directory_path", required=True, type=str)
@click.pass_context
def export(ctx: TQ42CliContext, dataset_id: str, directory_path: str) -> None:
    dataset = Dataset(client=ctx.obj.client, id=dataset_id)
    dataset.export(directory_path=directory_path)
