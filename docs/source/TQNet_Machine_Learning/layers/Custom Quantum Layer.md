
OBJECTIVES:
{x} validate Introduction
{x} validate Key Benefits - need supplementary info
{} include architecture, diagrams, reference -> unavailable, Anya checked AR team's Github pages and TQml docstrings
{x} Anya and Reuben have discussed the types of gates available
{x} validate Hyperparams, 1-Qubit hyperparams, 2-Qubit hyperparams
{x} validate UNCLEAR section
{x} validate python code snippet -> use a regression example, not a time series!
{x} add comments to jupyter notebook
{} validate jupyter notebook


# Custom Quantum Layer
## Introduction to CQ

The Custom Quantum (CQ) layer is a novel approach designed to integrate quantum layers with classical neural network layers, creating a syngergistic hybrid model. The CQ layer leverages the non-linear transformations inherent in quantum circuits to express a wide range of functions, creating a richer and more stable representation of the input data, which can then be further distilled by subsequent classical layers. The CQ approach is highly flexible and allows for complete control over the design of the quantum circuit. 

This architecture offers unprecedented expressivity of complex data features and navigation of critical challenges in high-dimensional search spaces (such as vanishing gradients and barren plateaus) – representing a path forward in the development of more powerful, efficient, and adaptable machine learning models for complex real-world problems. 

[Reference](https://arxiv.org/pdf/2008.08605)

## Key Benefits

- Enhanced Expressivity: The CQ layer leverages quantum circuits to perform non-linear transformations on input data, accessing a rich frequency spectrum that allows for more complex feature representation than classical neural network layers alone. 
- Mitigation of Training Obstacles: By enabling precise control over circuit design, the CQ layer helps address vanishing gradients and barren plateaus - common challenges in both quantum and deep classical neural networks. This allows for more effective training, even in deep hybrid architectures.
- Efficient High-Dimensional Data Processing: The quantum nature of the CQ layer allows it to navigate large search spaces more efficiently than classical approaches, making it particularly well-suited for high-dimensional data problems.
- Complementary to Classical Layers: When stacked with classical neural network layers, the CQ layer acts as a powerful feature extractor. It provides a rich, non-linear transformation of the input data that can then be further refined by classical layers, resulting in a distilled representation of the most relevant features.
- Customizable Feature Extraction: The flexibility to design any desired quantum circuit within the CQ layer allows users to tailor the feature extraction process to specific problem domains or data structures.
- Noise Resilience: The non-linear transformations performed by the CQ layer can help in extracting stable features from noisy data, which can then be further processed by classical layers to produce a clean, precise representation of the underlying patterns.
- Lightweight yet Powerful Models: By combining the expressive power of quantum circuits with the proven effectiveness of classical neural networks, hybrid models incorporating the CQ layer can achieve high performance with potentially fewer total parameters than purely classical approaches.
- Potential for universal function approximation


## Hyperparameters and Default Settings
The following hyperparameters are included in the CQ layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter | Description                                                                                                                                                           | Syntax           | Range                             | Default           |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|-----------------------------------|-------------------|
| n_qubits       | Number of qubits in each quantum circuit. <br/>For best results, formulate `n_qubits` as a power of 2.                                                                | int              | 2 to 8                            | 4                 |
| gates          | A list of quantum gates, where each gate has its own set of parameters. The choice and order of gates determines the quantum operations performed on the input data. Can be `Rotation`, `Hadamard` or `CNOT`. | list of objects |  (see below tables) |  (see below tables)       |

# 1-Qubit Gate Hyperparameters
| Hyperparameter | Description                                                                                                                                                                                                          | Syntax | Range    | Default  |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|----------|
| variational    | Controls the number of iterations for the quantum algorithm used to train the quantum layer. The variational algorithm optimizes the quantum circuit parameters to minimize a cost function.                         | int    | 1 to 100 | 12       |
| encoding       | Specifies the encoding method used to represent classical data in the quantum circuit. Different encoding techniques may be suitable for different types of problems. Can be `method1`, `method2` or `method3`.      | int    | 1 to 3   | 2        |
| measurement        | Pauli measurement that will be used at the end of each circuit for a particular qubit. Can be `X`, `Y` or `Z`.                                    | str    | `X` `Y` `Z`                       | `Y`               | -> this is the WINNER
 qubits in each circuit will be measured. If set to 'None' each qubit will be measured  | str    | 'single', 'even', 'None' | 'None' |
| wire           | Specifies which qubit(s) a particular gate should be applied to. Indicates the qubit index.                                                                                                                          | int   | [0, n_qubits-1] | 0 |

# 2-Qubit Gate Hyperparameters
| Hyperparameter | Description                                                                                                                                                                                                      | Syntax | Range    | Default  |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|----------|
| variational    | Controls the number of iterations for the quantum algorithm used to train the quantum layer. The variational algorithm optimizes the quantum circuit parameters to minimize a cost function.                     | int    | 1 to 100 | 12       |
| encoding       | Specifies the encoding method used to represent classical data in the quantum circuit. Different encoding techniques may be suitable for different types of problems. Can be `method1`, `method2` or `method3`.  | int    | 1 to 3   | 2        |
| measurement        | Pauli measurement that will be used at the end of each circuit for a particular qubit. Can be `X`, `Y` or `Z`.                                    | str    | `X` `Y` `Z`                       | `Y`               | -> this is the WINNER
| wire           | Specifies which qubit(s) a particular gate should be applied to. Indicates the indices of the two qubits.                                                                                                        | int    | [0, n_qubits-1] | 0 |


## Sample Python Code Block

Here is an example of how to apply the custom quantum layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a custom quantum layer with a classical dense layer. -> regression problem

```python
from google.protobuf.json_format import MessageToDict
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.compute import HardwareProto
from tq42.algorithm import (
    TrainDataProcessingParametersProto,
    OptimProto,
    LossFuncProto,
    DatasetStorageInfoProto,
    GenericMLTrainMetadataProto,
    GenericMLTrainParametersProto,
    Layer,
    ClassicalDenseLayer,
    MLModelType,
    TrainModelInfoProto,
    MLTrainInputsProto,
    AlgorithmProto,
    MeasureProto,
    CustomQuantumLayer,
    CnotGate,
    HadamardGate,
    VariationalGate,
    EncodingGate,
    MeasurementGate,
    Gate
)

custom_quantum_layer_msg = CustomQuantumLayer(
    num_qubits=2,
    gates=[
        Gate(hadamard=HadamardGate(wire=0)),
        Gate(hadamard=HadamardGate(wire=1)),
        Gate(variational=VariationalGate(wire=0, rotation=MeasureProto.X)),
        Gate(
            encoding=EncodingGate(wire=1, rotation=MeasureProto.Y, feature_id=0)
        ),
        Gate(cnot=CnotGate(wire1=0, wire2=1)),
        Gate(variational=VariationalGate(wire=1, rotation=MeasureProto.X)),
        Gate(measurement=MeasurementGate(wire=0, pauli=MeasureProto.X)),
        Gate(measurement=MeasurementGate(wire=1, pauli=MeasureProto.X)),
    ],
)

env_msg = GenericMLTrainMetadataProto(
    parameters=GenericMLTrainParametersProto(
        model_type=MLModelType.MLP,
        layers=[
            Layer(custom_quantum_layer=custom_quantum_layer_msg),
            Layer(classical_dense_layer=ClassicalDenseLayer(hidden_size=1, bias=True)),
        ],
        num_epochs=1,
        k_fold=1,
        batch_size=128,
        learning_rate=0.01,
        optim=OptimProto.ADAM,
        loss_func=LossFuncProto.MAE,
        train_model_info=TrainModelInfoProto(
            name="local_test",
            description="a_description",
        ),
        data_processing_parameters=TrainDataProcessingParametersProto(
            input_columns=[0, 1, 2, 3], output_columns=[4], timestamp_columns=[]
        ),
    ),
    inputs=MLTrainInputsProto(
        data=DatasetStorageInfoProto(storage_id="ENTER_DATASET_STORAGE_ID_HERE")
    ),
)

with TQ42Client() as client:
    client.login()
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.GENERIC_ML_TRAIN,
        experiment_id=exp.id,
        compute=HardwareProto.SMALL,
        parameters=MessageToDict(env_msg, preserving_proto_field_name=True)
    )

    print(run.data)

    result = run.poll()

    print(result.data)

```
