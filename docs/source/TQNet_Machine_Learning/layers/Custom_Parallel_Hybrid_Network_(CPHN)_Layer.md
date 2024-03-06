# Custom Parallel Hybrid Network (CPHN) Layer
## Introduction to CPHN
The Custom Parallel Hybrid Network Layer represents a tunable version of the Parallel Hybrid Network Layer, imbuing the network with increased adaptability and functionality. This network allows one to replace a quantum part of the PHN with a quantum layer from TQnet library.

It supports the incorporation of a multilayer perceptron into the classical part. The multilayer perceptron, a fundamental component in artificial neural networks, can be customized according to user specifications regarding the number of layers and neurons within each layer.

<<<<<<< HEAD
![CPHN layer architecture.png](../images/CPHN_layer_architecture.png)
=======
![CPHN layer architecture.png](../images/CPHN%20layer%20architecture.png)

[Documentation](https://refactored-train-y27rprg.pages.github.io/autoapi/tqml/tqnet/layers/index.html#tqml.tqnet.layers.CPHN) and [source code](https://refactored-train-y27rprg.pages.github.io/_modules/tqml/tqnet/layers.html#CPHN).
>>>>>>> 7baba81 (grpc update)

## Key Benefits
- One of the most significant features of the Custom Parallel Hybrid Network is its ability to integrate any quantum layer from the TQnet library into its quantum part.
- Equally important is its capability to accept a user-defined multilayer perceptron within the classical part of the network. Users can specify the number of layers and neurons within each layer, offering a high degree of customization and adaptability.

## Hyperparameters and Default Settings
The following hyperparameters are included in the CPHN layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter | Description                                                                                                                                                     | Syntax | Range    | Default  |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|----------|
| q_part         | This is the Quantum Layer that will represent Quantum part of the layer. For example, `l = layers.DHN(30, layers.QDI(12, 4, 3), [10, 12], 4)`                   | int    | [12,4,3] | [12,4,3] |
| n_qubits       | Number of qubits in each quantum circuit. <br/>Note that `in_features` must be divisible by `n_qubits`. For best results, formulate `n_qubits` as a power of 2. | int    | 1 to 25  | 5        |
| depth          | Number of variational layers inside one quantum circuit.                                                                                                        | int    | 1 to 30  | 4        |
| hidden_dim     | List of classical linear part dimensions.                                                                                                                       | int    | [4, 16]  | [4, 16]  |


## Quantum Circuit Representation
This circuit diagram reflects some of the default settings listed above, plus 12 input features. To visualize a dynamic graph, please use the TQ42 web interface.

<<<<<<< HEAD
![CPHN circuit diagram example.png](../images/CPHN_circuit_diagram_example.png)
=======
![CPHN circuit diagram example.png](../images/CPHN%20circuit%20diagram%20example.png)
>>>>>>> 7baba81 (grpc update)

## Sample Python Code Block
Here is an example of how to apply the CPHN layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single CPHN layer:

```python
from tq42.algorithm import (
    DatasetStorageInfoProto,
    GenericMLTrainMetadataProto,
    GenericMLTrainParametersProto,
    Layer,
    MLTrainInputsProto,
    CPHNLayer,
    EFQLayer,
    QuantumLayer,
    MeasurementModeProto,
    EntanglingProto,
    MeasureProto,
    DiffMethodProto,
    QubitTypeProto,
)
from google.protobuf.json_format import MessageToDict

efq_layer = QuantumLayer(
    efq_layer=EFQLayer(
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
            Layer(cphn_layer=CPHNLayer(
                  quantum_layer=efq_layer,
                  hidden_size=2)
            )
        ],
    ),
    inputs=MLTrainInputsProto(
        data=DatasetStorageInfoProto(storage_id="random-uuid-with-training-data-inside")
    )
), preserving_proto_field_name=True)
<<<<<<< HEAD
```
=======
```
>>>>>>> 7baba81 (grpc update)
