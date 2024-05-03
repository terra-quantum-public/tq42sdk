# Submitting and Monitoring a Run

## Submitting an Experiment Run

When you are ready to begin your experiment run, use the `ExperimentRun` class and provide the following flags:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    client.login()

    experiment_run = ExperimentRun.create(
        client=client,
        experiment_id="<YOUR_EXP_ID>",
        compute="<COMPUTE>",
        algorithm="<ALGORITHM>",
        parameters="<PARAMETERS_JSON>"
    )
    print(experiment_run)
```

The preceding command consists of the following elements:

- `experiment_id` is a flag set to an experiment to which the run should be assigned.

- `compute` is a flag set to the pre-configured compute infrastructure you selected.

- `algorithm` is a flag set to the algorithm name that should solve the problem.

- `parameters` is a flag set to a JSON object containing constraints, hyperparameters, and possibly a URL for vectorized data or an objective function. For more details on how to prepare and structure your parameter code, please reference the developer guide for the specific algorithm and application or use case you are solving.

The result of this experiment creation is an `ExperimentRun` instance.

For example:

```python
from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

params = {
    'parameters': {
        'dimensionality': 2,
        'maximal_rank': 1,
        'points_number': 1,
        'quantization': True,
        'tolerance': 3.9997,
        'iteration_number': 1,
        'grid': [1, 2, 3],
        'limits': [1, 2, 3, 4, 5, 6],
        'objective_function': 'http://34.32.169.11:8000/test_func_eval/Ackley/'
    },
    'inputs': {}
}

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.TETRA_OPT,
        experiment_id="<YOUR_EXP_ID>",
        compute=HardwareProto.SMALL,
        parameters=params
    )
    print(run)
```

## Monitoring an Experiment Run

After you submit, the system will begin processing the run. You can monitor its status in one of two ways:

You can use the `poll` function on the `ExperimentRun` instance to monitor an experiment run until it completes:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    run = ExperimentRun(client=client, id="<YOUR_EXP_RUN_ID>").poll()
    print(run)
```

Alternatively, you can check on the status of a run at any time by using the `check`
method of the `ExperimentRun` instance like:
```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    run = ExperimentRun(client=client, id="<YOUR_EXP_RUN_ID>").check()
    print(run)
```

The system will return the instance itself with updated data.


## Cancelling an Experiment Run

To cancel a run that is `QUEUED`, `PENDING`, or `RUNNING`, type:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    run = ExperimentRun(client=client, id="<YOUR_EXP_RUN_ID>").cancel()
    print(run)
```

If the run has not completed when the cancellation request is submitted, the run will move into `CANCELLED_PENDING` status.

If the run has been fully cancelled, it will move into `CANCELLED` status;
however, if the result comes before the run was `CANCELLED` or `CANCELLED_PENDING`,
then the run will complete and the status will show `COMPLETED`.
