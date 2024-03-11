# Double Hybrid Network (DHN) Layer
## Introduction to DHN
The Double Hybrid Network Layer is an advanced architecture that builds upon the capabilities of previous layers such as the Parallel Hybrid Network Layer. Unlike earlier designs, this network facilitates distinct input paths for the quantum and classical components of the system. This flexibility allows for more refined control of data flow within the network, as the user can designate which part of the original vector will be inputted into the quantum section and which part into the classical section.

This capability offers a unique advantage, enabling the neural network to learn in a way that optimizes the processing of different patterns using quantum and classical neurons as needed.

Such an architecture is applicable in Physics-Informed Neural Networks (PINNs), which have demonstrated significant efficacy in solving differential equations.

![DHN layer architecture.png](../images/DHN_layer_architecture.png)

[Documentation](https://refactored-train-y27rprg.pages.github.io/autoapi/tqml/tqnet/layers/index.html#tqml.tqnet.layers.DHN) and [source code](https://refactored-train-y27rprg.pages.github.io/_modules/tqml/tqnet/layers.html#DHN).

## Key Benefits
- One of the standout features of the Double Hybrid Network is its ability to take in different parts of the original vector into the quantum and classical segments of the network.
- The user has the freedom to choose which segment of the vector goes where, enabling a customized blend of quantum and classical processing, optimizing the network's learning ability.

## Hyperparameters and Default Settings
The following hyperparameters are included in the DHN layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter | Description                                                                                                                                                                                        | Syntax | Range    | Default  |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|----------|
| q_part         | This is the Quantum Layer that will represent Quantum part of Double layer. `q_part` should have `CertainLayer` parent class. For example, `l = layers.DHN(30, layers.QDI(12, 4, 3), [10, 12], 4)` | int    | [12,4,3] | [12,4,3] |
| n_qubits       | Number of qubits in each quantum circuit. <br/>Note that `in_features` must be divisible by `n_qubits`. For best results, formulate `n_qubits` as a power of 2.                                    | int    | 1 to 25  | 5        |
| depth          | Number of variational layers inside one quantum circuit.                                                                                                                                           | int    | 1 to 30  | 4        |
| hidden_dim     | List of classical linear part dimensions. Note, that it should also include last dimension as it is not defined from the Quantum part in contrast with `CPHN`.                                     | int    | [16]     | 16       |
| from_classic   | Starting index for sublist that goes to the classical part.                                                                                                                                        | int    | 2 to 20  | 4        |


## Quantum Circuit Representation
This circuit diagram reflects some of the default settings listed above, plus 12 input features. To visualize a dynamic graph, please use the TQ42 web interface.

![DHN Circuit example.png](../images/DHN_Circuit_example.png)

## Sample Python Code Block
Here is an example of how to apply the DHN layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single DHN layer:

```python
from tq42.algorithm import (
    PQNLayer,
    DatasetStorageInfoProto,
    GenericMLTrainMetadataProto,
    GenericMLTrainParametersProto,
    Layer,
    MLTrainInputsProto,
    DHNLayer,
    QuantumLayer,
    MeasurementModeProto,
    EntanglingProto,
    MeasureProto,
    DiffMethodProto,
    QubitTypeProto,
)

from google.protobuf.json_format import MessageToDict

pqn_layer = QuantumLayer(
    pqn_layer=PQNLayer(
        in_features=8,
        num_qubits=2,
        depth=1,
        measurement_mode=MeasurementModeProto.Name(MeasurementModeProto.EVEN),
        rotation=MeasureProto.Name(MeasureProto.Z),
        entangling=EntanglingProto.Name(EntanglingProto.STRONG),
        measure=MeasureProto.Name(MeasureProto.Y),
        diff_method=DiffMethodProto.Name(DiffMethodProto.ADJOINT),
        qubit_type=QubitTypeProto.Name(QubitTypeProto.LIGHTNING_QUBIT),
    )
)

params = MessageToDict(GenericMLTrainMetadataProto(
    parameters=GenericMLTrainParametersProto(
        # ... TODO: add the other parameters of your choice
        layers=[
            Layer(dhn_layer=DHNLayer(
                  quantum_layer=pqn_layer,
                  hidden_size=8,
                  classical_start_index=4),
            )
        ],
    ),
    inputs=MLTrainInputsProto(
        data=DatasetStorageInfoProto(storage_id="random-uuid-with-training-data-inside")
    )
), preserving_proto_field_name=True)
```