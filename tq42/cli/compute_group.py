from dataclasses import asdict

import yaml

from tq42.compute import Compute, list_all, HardwareProto


def compute_group(args):
    if args.command == "list":
        return compute_list()

    elif args.command == "show-details":
        return compute_show_details(args)


def compute_list() -> str:
    details = [asdict(hw.show_details()) for hw in list_all()]
    return yaml.dump(details, default_flow_style=False, sort_keys=False)


def compute_show_details(args):
    # noinspection PyBroadException
    try:
        hardware = args.compute.upper()
        compute = Compute(hardware=HardwareProto.Value(hardware))
        details = asdict(compute.show_details())
        return yaml.dump(details, default_flow_style=False, sort_keys=False)
    except Exception:
        options_list = [key for key, val in HardwareProto.items() if val != 0]
        options = ", ".join(options_list)
        example = f"tq42 compute show-details --compute=[{options}]"
        return "Invalid command. \nUsage: " + example
