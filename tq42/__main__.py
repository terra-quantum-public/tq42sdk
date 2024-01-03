import sys
from tq42.exceptions import (
    NoDefaultError,
    InvalidArgumentError,
    NoMatchingAttributeError,
)
from tq42.cli.parsers.tq42parser import parse_args
from tq42.cli.tq42_all import tq42_all
from tq42.client import TQ42Client


def main():
    try:
        args = parse_args(sys.argv[1:])
        env_config_file = args.config
        with TQ42Client(env_config_file) as client:
            res = tq42_all(client, args)
            if res is not None:
                print(res)

    # If you want to catch specific CLI related exceptions
    # you can catch them here and specify custom CLI exception handling
    except NoDefaultError:
        raise NoDefaultError("tq42 {}".format(" ".join(sys.argv[1:]))) from None
    except NoMatchingAttributeError as e:
        raise InvalidArgumentError(
            "tq42 {}".format(" ".join(sys.argv[1:])), e.details
        ) from None

    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
