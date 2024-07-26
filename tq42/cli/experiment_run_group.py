import ast

import click

import tq42.cli.utils.cli_functions as cli
from tq42.cli.utils.types import TQ42CliContext
from tq42.experiment_run import ExperimentRun
from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto


@click.group("run", help="Command group to manage experiment runs")
def exp_run_group() -> click.Group:
    pass


@exp_run_group.command("cancel")
@click.argument("exp_run_id", required=True, type=str)
@click.pass_context
def cancel_run(ctx: TQ42CliContext, exp_run_id: str) -> None:
    res = cli.cancel_exprun(ctx.obj.client, exp_run_id)
    click.echo(res)


@exp_run_group.command("poll")
@click.argument("exp_run_id", required=True, type=str)
@click.pass_context
def poll_run(ctx: TQ42CliContext, exp_run_id: str) -> None:
    res = cli.poll_exprun(ctx.obj.client, exp_run_id)
    click.echo(res)


@exp_run_group.command("check")
@click.argument("exp_run_id", required=True, type=str)
@click.pass_context
def check_run(ctx: TQ42CliContext, exp_run_id: str) -> None:
    res = cli.get_exprun(ctx.obj.client, exp_run_id)
    click.echo(res)


@exp_run_group.command(
    "list", help="e.g. tq42 exp run list --exp 98ccb1d2-a3d0-48c8-b172-022f6db9be01"
)
@click.option("--exp", "exp_id", required=True, type=str)
@click.pass_context
def list_runs(ctx: TQ42CliContext, exp_id: str) -> None:
    res = cli.list_expruns(ctx.obj.client, exp_id)
    click.echo(res)


@exp_run_group.command(
    "create",
    help="e.g. tq42 exp run create --exp 98ccb1d2-a3d0-48c8-b172-022f6db9be01  --compute small --algorithm TETRA_OPT --parameters \"{'parameters': {'dimensionality':6,'maximal_rank' :1, 'points_number': 1, 'quantization' : True , 'tolerance':3.9997,  'grid': [1,2,3], 'upper_limits':[1,2,3,4,6,6], 'lower_limits': [0,0,0,0,0,0] , 'objective_function':'https://terraquantum.swiss', 'iteration_number': 1}, 'inputs': {}}\"",
)
@click.option("--exp", "exp_id", required=True, type=str)
@click.option("--compute", "compute", required=True, type=str)
@click.option("--algorithm", "algorithm", required=True, type=str)
@click.option("--parameters", "parameters", required=True, type=str)
@click.pass_context
def create_run(
    ctx: TQ42CliContext, exp_id: str, compute: str, algorithm: str, parameters: str
) -> None:
    algo = AlgorithmProto.Value(algorithm.upper())
    compute_val = HardwareProto.Value(compute.upper())
    params = ast.literal_eval(parameters)
    click.echo(
        ExperimentRun.create(
            client=ctx.obj.client,
            algorithm=algo,
            experiment_id=exp_id,
            compute=compute_val,
            parameters=params,
        ).data
    )
