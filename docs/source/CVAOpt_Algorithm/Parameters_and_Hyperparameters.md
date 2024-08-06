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

  Use channels to link a function evaluator to the optimization. Channels are implementing a so-called ask & tell interface where the optimizer sends the candidates to the channel and waits until the objective values are made available on the channel. More details on setting up a web service or a channel implementing a function evaluator can be found in [Objective Functions](../Objective_Functions/Objective_Function.md).

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

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.algorithm import AlgorithmProto
import asyncio
import numpy as np
from tq42.channel import Channel, Ask, Tell
import OptimizationTestFunctions as otf

cva_params = {}
cva_params['objectives'] = [{'name': 'Rosenbrock', 'aim_type': 'MINIMIZE'}]
cva_params['variables'] = []
cva_params['variables'].append({'name': 'x1', 'info_real': {'lower_bound': -1.0, 'upper_bound': 1.0}})
cva_params['variables'].append({'name': 'x2', 'info_real': {'lower_bound': -1.0, 'upper_bound': 1.0}})
cva_params['parameters'] = {}
cva_params['parameters']['max_generation'] = 50
cva_params['parameters']['mue'] = 2
cva_params['parameters']['lambda'] = 10

exp_id = "<YOUR_EXPERIMENT_ID>"


async def run_exp_with_channel(client, experiment_id, params):
  # set up channel
  channel = await Channel.create(client=client)
  # extend cva_params with func_eval_worker_channel_id
  params['func_eval_worker_channel_id'] = channel.id

  # create the experiment run
  run = ExperimentRun.create(
    client=client,
    algorithm=AlgorithmProto.CVA_OPT,
    experiment_id=experiment_id,
    compute=HardwareProto.SMALL,
    parameters={'parameters': params, 'inputs': {}}
  )

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

  def do_nothing():
    pass

  await channel.connect(
    callback=callback,
    finish_callback=do_nothing,
    max_duration_in_sec=None,
    message_timeout_in_sec=120
  )
  # return the run to retrieve the result    
  return run


with TQ42Client() as tq42client:
  loop = asyncio.get_event_loop()
  run = loop.run_until_complete(run_exp_with_channel(tq42client, exp_id, cva_params))
  result = run.poll()
```

You can find this example as a [jupyter notebook here](https://github.com/terra-quantum-public/tq42sdk/tree/main/notebooks). 