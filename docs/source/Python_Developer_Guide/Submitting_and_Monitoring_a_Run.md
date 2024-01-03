# Submitting and Monitoring a Run

## Submitting an Experiment Run

When you are ready to begin your experiment run, type use the `ExperimentRun` class and provide the following flags:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    client.login()

    ExperimentRun.create(
        client=client,
        exp="EXP_ID",
        compute="COMPUTE",
        algorithm="ALGORITHM",
        parameters="PARAMETERS_JSON"
    )
```

The preceding command consists of the following elements:

- `exp` is a flag set to an experiment to which the run should be assigned.

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
        'objective_function': 'http://34.32.169.11:8000/func_eval/'
    },
    'inputs': {}
}

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.TETRA_OPT,
        exp="ff573d1a-b759-4ca5-8fc6-43ed42567420",
        compute=HardwareProto.SMALL,
        parameters=params
    )
```

## Monitoring an Experiment Run

After you submit, the system will begin processing the run. You can monitor its status in one of two ways:

You can use the `poll` function on the `ExperimentRun` instance to monitor an experiment run until it completes:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    ExperimentRun(client=client, id="EXP_RUN_ID").poll()
```

For example:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    ExperimentRun(client=client, id="2852d0c7-2c5a-4d24-9e1e-f859c0dc6f81").poll()
```

Alternatively, you can check on the status of a run at any time by using the `check`
method of the `ExperimentRun` instance like:
```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    ExperimentRun(client=client, id="EXP_RUN_ID").check()
```

The system will return the instance itself with updated data.

For example:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    ExperimentRun(client=client, id="2852d0c7-2c5a-4d24-9e1e-f859c0dc6f81").check()
```


## Cancelling an Experiment Run

To cancel a run that is `QUEUED`, `PENDING`, or `RUNNING`, type:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    ExperimentRun(client=client, id="EXP_RUN_ID").cancel()
```

If the run has not completed when the cancellation request is submitted, the run will move into `CANCELLED_PENDING` status.

If the run has been fully cancelled, it will move into `CANCELLED` status; however, if the result comes before the run was `CANCELLED` or `CANCELLED_PENDING`, then the run will complete and the status will show `COMPLETED`.

For example:
```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    ExperimentRun(client=client, id="2852d0c7-2c5a-4d24-9e1e-f859c0dc6f81").cancel()
```
