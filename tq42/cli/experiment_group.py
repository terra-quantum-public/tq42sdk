import tq42.cli.cli_functions as cli
import tq42.utils.utils_for_cache as cache_utils
from tq42.cli.parsers.params_checker import check_params


def experiment_group(client, args):
    if args.command == "list":
        return exp_list_by_proj(client, args)

    elif args.command == "set-friendly-name":
        return exp_set_friendly_name(client, args)


def exp_list_by_proj(client, args):
    # TODO: Need to display error message to stderr when no proj is specified or set.
    #  Should do this by raising an exception and displaying from main function

    error_msg = "No project id is set. \nExample: tq42 exp list --proj b0edfd26-0817-4818-a278-17ef6c14e3a5"

    if args.proj is None:
        proj = cache_utils.get_current_value("proj")
        if proj == "":
            return error_msg
        else:
            return cli.list_exp_by_proj(client, proj)

    return cli.list_exp_by_proj(client, args.proj)


def exp_set_friendly_name(client, args):
    check_params("exp set-friendly-name", args)
    return cli.exp_update(client, args)
