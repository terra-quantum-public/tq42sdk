# Parameters and Hyperparameters

There are two sets of parameters, one to define the optimization problem to be solved, the other to control the behaviour of the optimization algorithm.

## Parameters to define the optimization problem

* objectives: List of objectives

  An objective is defined by
  * name : The name of the objective
  * aim: The aim of the objective, one of
    * MINIMIZE: for minimizing
    * MAXIMIZE: for maximizing
    * VALUE: optimize for a specific target value
  * aim_value: the specific target value, it has only be provided for the aim VALUE

* variables: List of input variables (or design parameters)

  A variable consists of two entries
  * name: The name of the variable
  The second entry defines the lower and upper bound in case of real or integer variables and for class variables a list of possible class values has to be provided. Dependent on the varibale type these entries are:
  * info_real: A dictionary with two entries: lower_bound and upper_bound
  * info_int: A dictionary with two entries: lower_bound and upper_bound
  * info_class: A dictionary with entry values which is a list of possible class values as strings

* function evaluation

  There are two possibilities to link a function evaluator to the optimization. One is to set a function worker url implementing a web service which sends back immediately the objective values after receiving candidate solutions. The other way is to use channels. Channels are implementing a so called ask & tell interface where the optimizer sends the candidates to the channel and waits until the objective values are made available on the channel. More details on setting up a web service or a channel implementing a function evaluator can be found in [Objective Functions](../Objective_Functions/Objective_Function.md).

 * func_eval_worker_url: The URL of the function evaluation worker
 * func_eval_worker_channel_id: The id returned by the channel

## Parameters to control the algorithm
These parameters are optional and will be set to default values when they are not provided to the optimization algorithm.

The parameters for cva are:

* MaxGeneration 

The number of iterations after the optimization algorithms stops

* Mue

The number of parents in a iteration

* Lambda

The number of offsprings created in a iteration

## Example

### Example using a function eval worker url
```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.compute import HardwareProto
from tq42.algorithm import (
    AlgorithmProto,
    CvaOptMetadataProto,
    CvaOptParametersProto,
    CvaOptInputsProto
)
from google.protobuf.json_format import MessageToDict


func_eval_worker_ip = '34.32.169.11'
# single-objective optimization
func_eval_worker_url_sphere = 'http://' + func_eval_worker_ip + ':8000/test_func_eval/Sphere'
# multi-objective optimization
func_eval_worker_url_zdt1 = 'http://' + func_eval_worker_ip + ':8000/test_func_eval/ZDT1'


with TQ42Client() as client:
    params = MessageToDict(CvaOptMetadataProto(
        parameters=CvaOptParametersProto(
            objectives = [{'name': 'Sphere', 'aim_type': 'MINIMIZE'}],
            variables = [{'name': 'x1', 'info_real': {'lower_bound': -1.0, 'upper_bound': 1.0}},
                         {'name': 'x2', 'info_real': {'lower_bound': -1.0, 'upper_bound': 1.0}}],
            func_eval_worker_url = func_eval_worker_url_sphere,
            parameters = {'max_generation': 250, 'mue': 15, 'lambda' : 100},
            ),
        inputs=CvaOptInputsProto(),
    ), preserving_proto_field_name=True)

    ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.CVA_OPT,
        experiment_id="your_experiment_id",
        compute=HardwareProto.SMALL,
        parameters=params,
    )
```

### Example using a channel to evaluate the objective function
```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.organization import list_all as list_all_organizations
from tq42.project import list_all as list_all_projects
from tq42.experiment import list_all as list_all_experiments
from tq42.experiment_run import ExperimentRunStatusProto
from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto
import json
import pandas
import asyncio
import numpy as np
from tq42.channel import Channel, Ask, Tell
import OptimizationTestFunctions as otf

cva_params = {}
cva_params['objectives'] = [{'name': 'Rosenbrock', 'aim_type':'MINIMIZE'}]
cva_params['variables'] = []
cva_params['variables'].append({'name': 'x1', 'info_real':{'lower_bound':-1.0, 'upper_bound':1.0}})
cva_params['variables'].append({'name': 'x2', 'info_real':{'lower_bound':-1.0, 'upper_bound':1.0}})
cva_params['parameters'] = {}
cva_params['parameters']['max_generation'] = 50
cva_params['parameters']['mue'] = 2
cva_params['parameters']['lambda'] = 10

async def run_exp_with_channel(client, experiment_id, cva_params):
    # set up channel
    channel = await Channel.create(client=client)
    # extend cva_params with func_eval_worker_channel_id
    cva_params['func_eval_worker_channel_id'] = channel.id
    
    # create the experiment run
    run = ExperimentRun.create(
        client=client, 
        algorithm=AlgorithmProto.CVA_OPT, 
        experiment_id="your_experiment_id",
        compute=HardwareProto.SMALL,
        parameters={'parameters': cva_params, 'inputs': {} }
    )
    print(f\" starting run with id {run.id}\")

    # define the callback function
    async def callback(ask: Ask) -> Tell:
        dim = len(ask.headers)
        func = otf.Rosenbrock(dim)
        print('callback received parameters of length: ' + str(len(ask.parameters)))
        y = []
        for parameter in ask.parameters:
            y.append(float(func(np.array(parameter.values))))
        # add result to data

        return Tell(
            parameters=ask.parameters,
            headers=ask.headers,
            results=y
        )
    # define a function to be called after the optimization is finished
    def success():
        pass

    # let the channel wait for connections
    is_finished = False
    max_retries = 10
    retries = 0
    while (not is_finished) and (retries < max_retries):
        await channel.connect(
                callback=callback,
                finish_callback=success,
                max_duration_in_sec=None,
                message_timeout_in_sec=120
            )
        retries += 1
        run_state = run.check().data.status
        if ExperimentRunStatusProto.Name(run_state) in ['CANCELLED', 'COMPLETED', 'FAILED', 'CANCEL_PENDING']:
            is_finished = True
        else:
            print('run is in state ' + ExperimentRunStatusProto.Name(run_state) + ', continuing')
    # return the run to retrieve the result    
    return run

run = await run_exp_with_channel(tq42client, experiment_id, cva_params)
```
