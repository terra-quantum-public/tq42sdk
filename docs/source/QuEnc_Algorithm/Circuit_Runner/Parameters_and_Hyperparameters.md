Submitting a Circuit Run experiment using different QPUs and simulators
-------------------------

# Parameters
The following parameters are required for the TQ42 QuEnc Algorithm to create a circuit:

- shots: int
  - The number of times a quantum circuit is executed or run on a quantum computer or simulator.
- backend: string
  - The specific CPU or simulator to be used.

Note: TQ42 QuEnc creates a circuit.json file which can be referenced by using the circuit storageId inside a circuit runner experiment.

## Creating a circuit using the Command Line Interface (CLI):  

```bash
tq42 exp run create --exp  0ba18e6f-65e6-4c0a-bda3-091c5a45312d --compute small --algorithm CIRCUIT_RUN --parameters "{'parameters': {'shots': '500', 'backend':  'QISKIT_SIMULATOR'}, 'inputs': {'storage_id' : 'a_random_storage_id'}}"
```                                                                                                                                                                      

## Creating a circuit using the Python Application Programming Interface (API):

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun, HardwareProto
from tq42.algorithm import AlgorithmProto

parameters = {
    'parameters': {
        'shots': 500,
        'backend': 'CIRQ_SIMULATOR'
    },
    'inputs': {
        'circuit': {'storage_id': 'a_random_storage_id'}
    }
}

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.CIRCUIT_RUN,
        experiment_id="1cd18e6f-65e6-4c0a-bda3-091c5a45412c",
        compute=HardwareProto.SMALL,
        parameters=parameters
    )

    print(run)
```


