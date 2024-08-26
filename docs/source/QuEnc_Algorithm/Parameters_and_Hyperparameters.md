Creating a Quantum Circuit using TQ42 QuEnc and Running on different Quantum Processing Unit(QPU)
-------------------------

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

parameters = {
    'parameters': {
        'circuit_type': 'sim_qk_dense',
        'qubo': [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        'number_layers': 5,
        'steps': 25,
        'velocity': 0.05,
        'optimizer': 'ADAM'
    },
    'inputs': {}
}

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        algorithm='QUENC',
        version='0.4.0',
        experiment_id="EXP_ID",
        compute=HardwareProto.SMALL,
        parameters=parameters
    )

print(run)
```

TQ42 QuEnc creates a circuit.json file that can then be fed to the TQ42 Circuit Runner while specifying the number of shots for the backend provider.
