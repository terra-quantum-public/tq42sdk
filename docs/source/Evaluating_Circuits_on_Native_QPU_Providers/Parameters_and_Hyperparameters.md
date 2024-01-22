Creating a Quantum Circuit using TQ42 QuEnc and Running on different Quantum Processing Unit(QPU)
-------------------------
![img.png](../images/maxcut.png)  
Example problem:  

Max-cut

Let us consider the simple unweighted max-cut problem which is depicted in the figure. The goal of unweighted max-cut problem separate vertices into two groups so that number of edges between of two groups has the maximum value. In the figure, we highlighted the solution as the white vertices are in one group and the black ones in another group. This spliting is a solution because of all edges connect vertices from different groups so we can not add one more edge to a solution.  

## Getting a solution using TQ42 QuEnc  
QuEnc returns a binary vector where the same values of vector mean the vertices are in the same group. Note that we don't choose the value for every group so reversing bits in the vector get the same solution ([1, 0, 1, 1, 0] and [0, 1, 0, 0, 1] are the same).

We can create a Quantum Circuit using QuEnc and be able to run it on different Quantum Processing Unit(QPU) providers.

To get a solution, we must first create a circuit using QuEnc then run that circuit using an IONQ or IBM QPU.  

# Parameters
For the parameters required for the TQ42 QuEnc Algorithm to create a circuit:

- circuit_type: string   
('sim_cirq_dense' or 'sim_qk_dense')   
Note: QuEnc works faster with CIRQ library(sim_cirq_dense).
- qubo: list of floats  
- number_layers: int  
- steps: int  
- velocity: float  
- saved_circuit: bool
- optimizer: string   
('Momentum', 'ADAM', 'hessian', 'natural gradient')

## Creating a circuit using the Command Line Interface (CLI):  

```bash
tq42 exp run create --exp  0ba18e6f-65e6-4c0a-bda3-091c5a45312d --compute small --algorithm TETRA_QUENC --parameters "{'parameters': {'circuit_type': 'sim_qk_dense', 'qubo':  [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]}, 'inputs': {}}'
```                                                                                                                                                                      

## Creating a circuit using the Python Application Programming Interface (API):

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.compute import HardwareProto
from tq42.algorithm import AlgorithmProto

parameters = {
    'parameters': {
        'circuit_type': 'sim_qk_dense',
        'qubo': [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        'number_layers': 5,
        'steps': 25,
        'velocity': 0.05,
        'saved_circuit': True,
        'optimizer': 'ADAM'
    },
    'inputs': {}
}

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.TETRA_QUENC,
        experiment_id="EXP_ID",
        compute=HardwareProto.SMALL,
        parameters=parameters
    )

print(run)
```

TQ42 QuEnc creates a circuit.json file that we can then feed to the TQ42 Circuit Runner to ba able to specify the number of shots we want and the backend provider.


Running the circuit created on different QPU providers using TQ42 Circuit Runner
-------------------------
For the parameters required for the CIRCUIT_RUN Algorithm:

- shots: int  

- backend: string   
('IBM', 'IONQ')

Currently we can run on either an IBM or IONQ backend. To choose, we need to specify it using the "backend" parameters:  

## Using the CLI:

```bash
tq42 exp run create --exp c385c53b-38c2-4036-9823-50ce932a9b34  --compute small --algorithm CIRCUIT_RUN --parameters "{'parameters': {'shots':500, 'backend':'IONQ'}, 'inputs': {'circuit': {'storage_id': 'CIRCUIT_BUCKET_UUID'}}}"
```

## Using the API:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.compute import HardwareProto
from tq42.algorithm import AlgorithmProto

parameters = {
    'parameters': {
        'shots': 500,
        'backend': 'IONQ'
    },
    'inputs': {
        'circuit': {'storage_id': 'CIRCUIT_BUCKET_UUID'}
    }
}

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.CIRCUIT_RUN,
        experiment_id="EXP_ID",
        compute=HardwareProto.SMALL,
        parameters=parameters
    )
```
