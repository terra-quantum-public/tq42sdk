# Parallel Quantum Network (PQN) Layer
## Introduction to PQN
The Parallel Quantum Network layer includes multiple independent variational quantum circuits, where each parameterized quantum circuit is composed of three parts: angle-embedding, variational gates, and measurement. By employing a parallel quantum network layer, the system can process different subsets of features simultaneously, in parallel.

![PQN Layer Diagram]((PQN_Layer_Diagram.png))

Reference: https://arxiv.org/abs/2304.09224

[Documentation](https://refactored-train-y27rprg.pages.github.io/autoapi/tqml/tqnet/layers/index.html#tqml.tqnet.layers.PQN) and [source code](https://refactored-train-y27rprg.pages.github.io/_modules/tqml/tqnet/layers.html#PQN).

## Key Benefits
- Each quantum circuit within the parallel quantum network layer employs variational parameters exclusive to it, making the model more performant and adaptable across diverse datasets.
- This model featuring parallel quantum circuits is particularly effective in the Noisy Intermediate-Scale Quantum (NISQ) era, where executing computations with circuits comprising a large number of qubits is a challenge. Independent parallel quantum circuits are particularly effective in the current Noisy Intermediate-Scale Quantum (NISQ) era of quantum computing where employing large numbers of qubits in a single circuit is experimentally challenging.

## Hyperparameters and Default Settings
The following hyperparameters are included in the PQN layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter   | Description                                                                                                                                                                                                                                                                                                                   | Syntax | Range                             | Default           |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------|-------------------|
| in_features      | Number of features in the data.                                                                                                                                                                                                                                                                                               | int    | 1 to INT MAX                      |                   |
| n_qubits         | Number of qubits in each quantum circuit. <br/>Note that `in_features` must be divisible by `n_qubits`. For best results, formulate `n_qubits` as a power of 2.                                                                                                                                                               | int    | 1 to 32                           | 4                 |
| depth            | Number of variational layers inside one quantum circuit.                                                                                                                                                                                                                                                                      | int    | 1 to 30                           | 4                 |
| measurement_mode | Type of CNOTs configuration before measurement. <br/>When set to `single`, CNOTs would be applied at the end of each circuit and reduce the whole output dimension by `n_qubits` times. <br/>If set to `even` only (0, 2, 4, ...) qubits in each circuit will be measured. <br/>If set to `none` each qubit will be measured. | str    | `single` `even` `none`            | `none`            |
| rotation         | Type of embedding rotations used. Can be `X`, `Y` or `Z`.                                                                                                                                                                                                                                                                     | str    | `X` `Y` `Z`                       | `Z`               |
| entangling       | Type of entangling layer used. Can be `strong` or `basic`.                                                                                                                                                                                                                                                                    | str    | `strong` `basic`                  | `strong`          |
| measure          | Pauli measurement that will be used at the end of each circuit. Can be `X`, `Y` or `Z`.                                                                                                                                                                                                                                       | str    | `X` `Y` `Z`                       | `Y`               |
| diff_method      | Defines method for calculating gradients for quantum circuit. Must be either `adjoint` or `parameter-shift`.                                                                                                                                                                                                                  | str    | `adjoint` `parameter-shift`       | `adjoint`         |
| qubit_type       | Defines qubit device for simulating a quantum circuit. Must be either `lightning.qubit` or `lightning.gpu`.                                                                                                                                                                                                                   | str    | `lightning.qubit` `lightning.gpu` | `lightning.qubit` |


## Quantum Circuit Representation
This circuit diagram reflects the default settings listed above, plus 12 input features. To visualize a dynamic graph, please use the TQ42 web interface.

![PQN Circuit Architecture Defaults](../images/PQN_Circuit_Architecture_defaults.png)

## Sample Python Code Block
Here is an example of how to apply the PQN layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single PQN layer:

```python
from tq42.algorithm import (
    Layer,
    PQNLayer,
    MeasurementModeProto,
    EntanglingProto,
    MeasureProto,
    DiffMethodProto,
    QubitTypeProto,

 )

layers=[
    Layer(pqn_layer=
          PQNLayer(in_features=20, 
                   num_qubits=4, 
                   depth=4, 
                   measurement_mode = MeasurementModeProto.NONE,
                   rotation=MeasureProto.Z,
                   entangling=EntanglingProto.STRONG,
                   measure=MeasureProto.Y,
                   diff_method=DiffMethodProto.ADJOINT,
                   qubit_type=QubitTypeProto.LIGHTNING_QUBIT))
]
```