import click

from tq42.client import TQ42Client


class TQ42CliObject(object):
    client: TQ42Client


class TQ42CliContext(click.Context):
    obj: TQ42CliObject
