import ast

import click

import tq42.cli.utils.cli_functions as cli
from tq42.cli.utils.types import TQ42CliContext
from tq42.experiment_run import ExperimentRun, HardwareProto


@click.group("run")
def exp_run_group() -> click.Group:
    """
    Class to run experiments and view results

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Submitting_and_Monitoring_a_Run.html#
    """
    pass


@exp_run_group.command("cancel")
@click.argument("exp_run_id", required=True, type=str)
@click.pass_context
def cancel_run(ctx: TQ42CliContext, exp_run_id: str) -> None:
    """
    Cancel a run that is QUEUED, PENDING, or RUNNING.

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Submitting_and_Monitoring_a_Run.html#cancelling-an-experiment-run
    """
    res = cli.cancel_exprun(ctx.obj.client, exp_run_id)
    click.echo(res)


@exp_run_group.command("poll")
@click.argument("exp_run_id", required=True, type=str)
@click.pass_context
def poll_run(ctx: TQ42CliContext, exp_run_id: str) -> None:
    """
    Monitor an experiment run until it completes, then automatically display the results (if there are no errors).

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Submitting_and_Monitoring_a_Run.html#monitoring-an-experiment-run
    """
    res = cli.poll_exprun(ctx.obj.client, exp_run_id)
    click.echo(res)


@exp_run_group.command("check")
@click.argument("exp_run_id", required=True, type=str)
@click.pass_context
def check_run(ctx: TQ42CliContext, exp_run_id: str) -> None:
    """
    Monitor run status.

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Submitting_and_Monitoring_a_Run.html#monitoring-an-experiment-run
    """
    res = cli.get_exprun(ctx.obj.client, exp_run_id)
    click.echo(res)


@exp_run_group.command("list")
@click.option(
    "--exp",
    "exp_id",
    required=True,
    type=str,
    help="Attribute the command to a particular experiment",
)
@click.pass_context
def list_runs(ctx: TQ42CliContext, exp_id: str) -> None:
    """
    List all the runs within an experiment you have permission to view.

    e.g. tq42 exp run list --exp 98ccb1d2-a3d0-48c8-b172-022f6db9be01

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Setting_Up_Your_Environment.html#list-all-runs-within-an-experiment
    """
    res = cli.list_expruns(ctx.obj.client, exp_id)
    click.echo(res)


@exp_run_group.command("create")
@click.option(
    "--exp",
    "exp_id",
    required=True,
    type=str,
    help="Attribute the command to a particular experiment",
)
@click.option(
    "--compute",
    "compute",
    required=True,
    type=str,
    help="Specify the compute resources to apply to the command",
)
@click.option(
    "--algorithm",
    "algorithm",
    required=True,
    type=str,
    help="Specify the algorithm to apply to the command",
)
@click.option(
    "--version",
    "version",
    required=True,
    type=str,
    help="Specify the version of the algorithm to apply to the command",
)
@click.option(
    "--parameters",
    "parameters",
    required=True,
    type=str,
    help="Specify the parameters to apply to the command",
)
@click.pass_context
def create_run(
    ctx: TQ42CliContext,
    exp_id: str,
    compute: str,
    algorithm: str,
    version: str,
    parameters: str,
) -> None:
    """
    Begin an experiment run.

    e.g. tq42 exp run create --exp 98ccb1d2-a3d0-48c8-b172-022f6db9be01  --compute small --algorithm TETRA_OPT --version 0.1.0 --parameters \"{'parameters': {'dimensionality':6,'maximal_rank' :1, 'points_number': 1, 'quantization' : True , 'tolerance':3.9997,  'grid': [1,2,3], 'upper_limits':[1,2,3,4,6,6], 'lower_limits': [0,0,0,0,0,0] , 'objective_function':'https://terraquantum.swiss', 'iteration_number': 1}, 'inputs': {}}\"

    https://docs.tq42.com/en/latest/CLI_Developer_Guide/Submitting_and_Monitoring_a_Run.html#submitting-an-experiment-run
    """
    compute_val = HardwareProto.Value(compute.upper())
    params = ast.literal_eval(parameters)
    click.echo(
        ExperimentRun.create(
            client=ctx.obj.client,
            algorithm=algorithm,
            version=version,
            experiment_id=exp_id,
            compute=compute_val,
            parameters=params,
        ).data
    )
