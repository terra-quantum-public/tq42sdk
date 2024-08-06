Creating a Quantum Circuit using TQ42 QuEnc and Running on different Quantum Processing Unit(QPU)
-------------------------
#### Example problem: Max-cut

![img.png](../images/maxcut.png)  

Let us consider the simple unweighted max-cut problem, depicted in the figure. The goal of the unweighted max-cut problem is to separate vertices into two groups so that the number of edges between the two groups is maximized. In the figure, we have highlighted the solution where the white vertices belong to one group and the black vertices belong to another. This separation constitutes a solution because all edges connect vertices from different groups, meaning no additional edge can be added without violating the solution.  

## Finding a solution using TQ42 QuEnc  
QuEnc returns a binary vector where the same values of the vector mean the vertices are in the same group. Note that we don’t choose the value for every group, so reversing bits in the vector yields the same solution ([1, 0, 1, 1, 0] and [0, 1, 0, 0, 1] are the same).

We can create a Quantum Circuit using QuEnc and run it on different Quantum Processing Unit (QPU) providers.

To obtain a solution, we must first create a circuit using QuEnc and then run that circuit using an IONQ, IBM, IBM_SIMULATOR or CIRQ_SIMULATOR QPU.  

# Parameters
The following parameters are required for the TQ42 QuEnc Algorithm to create a circuit:

- circuit_type: string   
  - This parameter specifies the type of quantum circuit to be generated, with options "sim_cirq_dense" or "sim_qk_dense". The choice of circuit type influences the efficiency and performance of the algorithm, with the CIRQ library generally offering faster execution.
- qubo: list of floats
  - The QUBO (Quadratic Unconstrained Binary Optimization) matrix represented as a list of floats. This matrix encodes the optimization problem to be solved by the quantum circuit.
- number_layers: int  
  - An integer indicating the number of layers in the quantum circuit. Increasing the number of layers can enhance the expressiveness of the circuit, potentially leading to better optimization performance.
- steps: int  
  - Specifies the number of optimization steps to be performed during the training process. More steps generally allow for finer optimization of the circuit parameters.
- velocity: float  
  - A float parameter influencing the optimization velocity, controlling the rate of convergence during the training process.
- saved_circuit: bool
  - A boolean parameter indicating whether to save the generated circuit for future use. Saving the circuit can be useful for repeated executions or analysis.
- optimizer: string   
  - Specifies the optimization algorithm to be used during circuit training. Options are "Momentum", "ADAM", "hessian", and "natural gradient", each with its own characteristics regarding convergence speed and stability.

## Creating a circuit using the Command Line Interface (CLI):  

```bash
tq42 exp run create --exp  0ba18e6f-65e6-4c0a-bda3-091c5a45312d --compute small --algorithm TETRA_QUENC --parameters "{'parameters': {'circuit_type': 'sim_qk_dense', 'qubo':  [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]}, 'inputs': {}}'
```                                                                                                                                                                      

## Creating a circuit using the Python Application Programming Interface (API):

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun, HardwareProto
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

TQ42 QuEnc creates a circuit.json file that can then be feed to the TQ42 Circuit Runner while specifying the number of shots for the backend provider.


Running the circuit created on different QPU providers using TQ42 Circuit Runner
-------------------------
For the parameters required for the CIRCUIT_RUN Algorithm:

- shots: int  

- backend: string   
('IBM', 'IBM_SIMULATOR', 'IONQ', 'CIRQ_SIMULATOR')

Currently we can run on either an IBM, IBM_SIMULATOR, IONQ or CIRQ_SIMULATOR backend. To choose, we need to specify it using the "backend" parameters:  

## Using the CLI:

```bash
tq42 exp run create --exp c385c53b-38c2-4036-9823-50ce932a9b34  --compute small --algorithm CIRCUIT_RUN --parameters "{'parameters': {'shots':500, 'backend':'IBM'}, 'inputs': {'circuit': {'storage_id': 'CIRCUIT_BUCKET_UUID'}}}"
```

## Using the API:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.algorithm import AlgorithmProto

parameters = {
    'parameters': {
        'shots': 500,
        'backend': 'IBM'
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
