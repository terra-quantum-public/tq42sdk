# Parameters and Hyperparameters

There are two sets of parameters, one to define the optimization problem to be solved, the other to control the behaviour of the optimization algorithm.

## Parameters to define the optimization problem

* func_eval_worker_url: The URL of the function evaluation worker

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
        ),
        preserving_proto_field_name=True,
    )

    ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.CVA_OPT,
        experiment_id="your_experiment_id",
        compute=HardwareProto.SMALL,
        parameters=params,
```