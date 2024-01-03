# Submitting and Monitoring a Run

## Submitting an Experiment Run

When you are ready to begin your experiment run, type `tq42 exp run create` and provide the following flags:
```bash
tq42 exp run create \
    --exp="EXP_ID" \
    --compute="COMPUTE_NAME" \
    --algorithm="ALGORITHM_NAME" \
    --parameters="PARAMETERS_JSON"
```

The preceding command consists of the following elements:

- `exp` is a `tq42` command group.

- `run` is an `exp` command group.

- `create` is a `run` command.

- `--exp` is a flag set to an experiment to which the run should be assigned.

- `--compute` is a flag set to the pre-configured compute infrastructure you selected.

- `--algorithm` is a flag set to the algorithm name that should solve the problem.

- `--parameters` is a flag set to a JSON object containing constraints, hyper parameters, and possibly a URL for vectorized data or an objective function. For more details on how to prepare and structure your parameter code, please reference the developer guide for the specific algorithm and application or use case you are solving.

The output is the following:

`run="RUN_ID"`

`status="STATUS"`

For example:
```bash
tq42 exp run create \
    --exp="ff573d1a-b759-4ca5-8fc6-43ed42567420" \
    --compute="small" \
    --algorithm="tetraopt" \
    --parameters="{'parameters': {'dimensionality':2,'iterationNumber' : 1, 'maximalRank' :1, 'pointsNumber' : 1, 'quantization' : True , 'tolerance':3.9997,  'iterationNumber': 1, 'grid': [1,2,3], 'limits':[1,2,3,4,5,6], 'objectiveFunction':'https://testdata.test'}, 'inputs': {}}"

run="2852d0c7-2c5a-4d24-9e1e-f859c0dc6f81"
status=QUEUED
```

## Monitoring an Experiment Run

After you submit, the system will begin processing the run. You can monitor its status in one of two ways: 

You can use the `poll` command to monitor an experiment run until it completes, then automatically display the results (if there are no errors) by typing `tq42 exp run poll "RUN_ID"`:
```bash
tq42 exp run poll "RUN_ID"
```

For example:
```bash
tq42 exp run poll "2852d0c7-2c5a-4d24-9e1e-f859c0dc6f81"
status="RUNNING"
result_json=""

org="5bac0b60-48d0-45cd-bf0a-39505b058106"
proj="Fleet Routing" (23e9715e-6f0e-4819-b9f2-88db9ef0a599)
exp="Routing Option 1" (e9a8fc1d-3a9b-4867-9812-d98db90c8b5a)
algorithm="tetraopt"
compute="small"
parameters="{'parameters': {'dimensionality':2,'iterationNumber' : 1, 'maximalRank' :1, 'pointsNumber' : 1, 'quantization' : True , 'tolerance':3.9997,  'iterationNumber': 1, 'grid': [1,2,3], 'limits':[1,2,3,4,5,6], 'objectiveFunction':'https://testdata.test'}, 'inputs': {}}"
created_by="97b6d1d8-8f3d-4b4e-b64c-a92b31f49120"
created_at=2023-06-30 12:48PM UTC
```

Alternatively, you can check on the status of a run at any time by typing `tq42 exp run check "RUN_ID"`:
```bash
tq42 exp run check "RUN_ID"
```

The system will return one of the following values:

1. `QUEUED` This is the default status, when the run has been submitted and is awaiting resources.

2. `PENDING` At this stage, the run is waiting for the necessary resources to begin processing. This is the last opportunity to cancel a run before it begins (at which point charges are incurred).

3. `RUNNING` The job is processing. You can cancel a run at this stage, but you will still be charged for the resources used thus far. Depending on the job size, the experiment run may complete before the cancellation can process.

4. `CANCELLED_PENDING` A cancellation was submitted to stop the experiment run, but the cancellation request has not fully processed yet. 

5. `CANCELLED` The experiment run was successfully cancelled.

6. `COMPLETED` The experiment run completed successfully.

7. `FAILED` The experiment run failed. This could be due to a variety of reasons, such as improperly formatted code, inadequate resources or other compute resource failures, budget exhaustion, etc.

For example:
```bash
tq42 exp run check "2852d0c7-2c5a-4d24-9e1e-f859c0dc6f81"
COMPLETED
```


## Cancelling an Experiment Run

To cancel a run that is `QUEUED`, `PENDING`, or `RUNNING`, type `tq42 exp run cancel "RUN_ID"`:
```bash
tq42 exp run cancel "RUN_ID"
```

If the run has not completed when the cancellation request is submitted, the run will move into `CANCELLED_PENDING` status.

If the run has been fully cancelled, it will move into `CANCELLED` status; however, if the result comes before the run was `CANCELLED` or `CANCELLED_PENDING`, then the run will complete and the status will show `COMPLETED`.

For example:
```bash
tq42 exp run cancel "2852d0c7-2c5a-4d24-9e1e-f859c0dc6f81"
status="CANCELLED_PENDING"

org="5bac0b60-48d0-45cd-bf0a-39505b058106"
proj="Fleet Routing" (23e9715e-6f0e-4819-b9f2-88db9ef0a599)
exp="Routing Option 1" (e9a8fc1d-3a9b-4867-9812-d98db90c8b5a)
algorithm="tetraopt"
compute="small"
parameters="{'parameters': {'dimensionality':2,'iterationNumber' : 1, 'maximalRank' :1, 'pointsNumber' : 1, 'quantization' : True , 'tolerance':3.9997,  'iterationNumber': 1, 'grid': [1,2,3], 'limits':[1,2,3,4,5,6], 'objectiveFunction':'https://testdata.test'}, 'inputs': {}}"
created_by="97b6d1d8-8f3d-4b4e-b64c-a92b31f49120"
created_at=2023-06-30 12:48PM UTC
```
