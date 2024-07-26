from dataclasses import asdict

import yaml
import click

from tq42.compute import Compute, list_all as list_all_computes, HardwareProto


@click.group("compute")
def compute_group() -> click.Group:
    pass


@compute_group.command("list")
def list_all():
    details = [asdict(hw.show_details()) for hw in list_all_computes()]
    click.echo(yaml.dump(details, default_flow_style=False, sort_keys=False))


@compute_group.command("show-details")
@click.argument("compute", required=True)
def show_details(compute: str):
    # noinspection PyBroadException
    try:
        hardware = compute.upper()
        compute = Compute(hardware=HardwareProto.Value(hardware))
        details = asdict(compute.show_details())
        click.echo(yaml.dump(details, default_flow_style=False, sort_keys=False))
    except Exception:
        options_list = [key for key, val in HardwareProto.items() if val != 0]
        options = ", ".join(options_list)
        example = f"tq42 compute show-details --compute=[{options}]"
        click.echo("Invalid command. \nUsage: " + example)
