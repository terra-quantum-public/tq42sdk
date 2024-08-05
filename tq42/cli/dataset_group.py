import click

from tq42.cli.utils.types import TQ42CliContext
from tq42.dataset import Dataset, list_all, DatasetSensitivityProto


@click.group("dataset")
def dataset_group() -> click.Group:
    """
    Class to manage datasets.

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Work_with_Datasets.html
    """
    pass


@dataset_group.command("create")
@click.option(
    "--proj",
    "proj_id",
    required=True,
    type=str,
    help="Attribute the command to a particular project",
)
@click.option(
    "--name", "name", required=True, type=str, help="The official name of the dataset"
)
@click.option(
    "--desc",
    "description",
    required=True,
    type=str,
    help="A friendly description of the dataset",
)
@click.option(
    "--sensitivity",
    "sensitivity",
    required=True,
    type=str,
    help="One of the following categories: PUBLIC, GENERAL, SENSITIVE, CONFIDENTIAL",
)
@click.option("--url", "url", required=False, type=str, help="A URL to the dataset")
@click.option(
    "--file",
    "file",
    required=False,
    type=str,
    help="A file (path) to upload to the dataset",
)
@click.pass_context
def create_dataset(
    ctx: TQ42CliContext,
    proj_id: str,
    name: str,
    description: str,
    sensitivity: str,
    url: str = None,
    file: str = None,
) -> None:
    """
    Create a dataset within a project.

    e.g.:
    - File upload: tq42 proj dataset create --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01 --name "Example Dataset Name" --desc "Example Description"  --file "/local/file/path/file.txt" --sensitivity "confidential"
    - Bucket transfer: tq42 proj dataset create --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01 --name "Example Dataset Name" --desc "Example Description"  --url "https://mydata.com/drive/my-drive" --sensitivity "confidential"

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Working_with_Datasets.html
    """

    click.echo(
        Dataset.create(
            client=ctx.obj.client,
            project_id=proj_id,
            name=name,
            description=description,
            url=url,
            file=file,
            sensitivity=DatasetSensitivityProto.Value(sensitivity.upper()),
        ).data
    )


@dataset_group.command("list")
@click.option(
    "--proj",
    "proj_id",
    required=True,
    type=str,
    help="Attribute the command to a particular project",
)
@click.pass_context
def list_datasets(ctx: TQ42CliContext, proj_id: str) -> None:
    """
    List all datasets within a project.

    e.g.: tq42 proj dataset list --proj 98ccb1d2-a3d0-48c8-b172-022f6db9be01

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Working_with_Datasets.html
    """
    click.echo(
        [
            dataset.data
            for dataset in list_all(client=ctx.obj.client, project_id=proj_id)
        ]
    )


@dataset_group.command("get")
@click.argument("dataset_id", required=True, type=str)
@click.pass_context
def get(ctx: TQ42CliContext, dataset_id: str) -> None:
    """
    Get a specific dataset.

    e.g.: tq42 proj dataset get 98ccb1d2-a3d0-48c8-b172-022f6db9be01

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Working_with_Datasets.html
    """
    click.echo(Dataset(client=ctx.obj.client, id=dataset_id).data)


@dataset_group.command(
    "export",
)
@click.argument("dataset_id", required=True, type=str)
@click.argument("directory_path", required=True, type=str)
@click.pass_context
def export(ctx: TQ42CliContext, dataset_id: str, directory_path: str) -> None:
    """
    Export a specific dataset.

    e.g.: tq42 proj dataset export 98ccb1d2-a3d0-48c8-b172-022f6db9be01 /Users/user1/Downloads

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Working_with_Datasets.html
    """
    dataset = Dataset(client=ctx.obj.client, id=dataset_id)
    dataset.export(directory_path=directory_path)
