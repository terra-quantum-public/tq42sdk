import click

from tq42.cli.utils.types import TQ42CliContext


@click.group("auth")
def auth_group() -> click.Group:
    """
    Group to manage authentication

    https://docs.tq42.com/en/latest/README.html#authentication
    """
    pass


@auth_group.command("login")
@click.pass_context
def login(ctx: TQ42CliContext) -> None:
    """
    Opens a browser window to confirm the MFA code, enter your TQ42 username and password to authenticate.
    To access TQ42 services with Python commands, you need a TQ42 account.
    When running TQ42 Python commands, your environment needs to have access to your TQ42 account credentials.

    https://docs.tq42.com/en/latest/README.html#authentication
    """
    ctx.obj.client.login()
