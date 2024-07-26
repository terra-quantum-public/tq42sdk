import click

from tq42.cli.utils.types import TQ42CliContext, TQ42CliObject
from tq42.client import TQ42Client
from .auth_group import auth_group
from .compute_group import compute_group
from .organization_group import organization_group
from .experiment_group import experiment_group
from .project_group import project_group
from .environment_group import environment_group


@click.group(
    help=(
        "Visit {} to access our help center, from where you can access help articles and video tutorials, report bugs, contact support and request improvements."
        "\n\n"
        "For TQ42SDK documentation, visit https://docs.tq42.com/en/latest/."
        "\n\n"
        "Mandatory commands:"
        "\n\n"
        "tq42 auth login"
        "\n\n"
        'tq42 exp run create --exp="EXP_ID" --compute="COMPUTE_NAME" --algorithm="ALGORITHM_NAME" --parameters="PARAMETERS_JSON"'
        "\n\n"
        "---"
        "\n\n"
        "All other command are optional."
    )
)
@click.option(
    "--config",
    "config_path",
    required=False,
    help="Set path to alternate configuration file location",
)
@click.version_option()
@click.pass_context
def cli(ctx: TQ42CliContext, config_path: str):
    ctx.ensure_object(TQ42CliObject)
    ctx.obj.client = TQ42Client(alt_config_file=config_path)


cli.add_command(auth_group)
cli.add_command(compute_group)
cli.add_command(organization_group)
cli.add_command(experiment_group)
cli.add_command(project_group)
cli.add_command(environment_group)


if __name__ == "__main__":
    # TODO: do we need this? Maybe for testing?
    cli()
