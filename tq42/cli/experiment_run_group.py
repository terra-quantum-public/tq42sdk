import ast

import tq42.cli.cli_functions as cli
from tq42.cli.parsers.params_checker import check_params
from tq42.experiment_run import ExperimentRun
from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto


def experiment_run_group(client, args):
    if args.subcommand == "cancel":
        return exp_run_cancel(client, args)

    elif args.subcommand == "create":
        return exp_run_create(client, args)

    elif args.subcommand == "check":
        return exp_run_check(client, args)

    elif args.subcommand == "list":
        return exp_run_list(client, args)

    elif args.subcommand == "poll":
        return exp_run_poll(client, args)


def exp_run_cancel(client, args):
    res = cli.cancel_exprun(client, args.run)

    return res


def exp_run_poll(client, args):
    res = cli.poll_exprun(client, args.run)

    return res


def exp_run_create(client, args):
    check_params("exp run create", args)
    algo = AlgorithmProto.Value(args.algorithm.upper())
    compute = HardwareProto.Value(args.compute.upper())
    params = ast.literal_eval(args.parameters)
    return ExperimentRun.create(
        client=client,
        algorithm=algo,
        experiment_id=args.exp,
        compute=compute,
        parameters=params,
    ).data


def exp_run_check(client, args):
    return cli.get_exprun(client, args.run)


def exp_run_list(client, args):
    check_params("exp run list", args)
    return cli.list_expruns(client, args.exp)
