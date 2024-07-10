
OBJECTIVES:
{} validate Introduction
{} validate Key Benefits - need supplementary info
{} include architecture, diagrams, reference -> unavailable, Anya checked AR team's Github pages and TQml docstrings
{} include quantum circuit representation -> unavailable, Anya checked AR team's Github pages and TQml docstrings
{} validate Hyperparams, 1-Qubit hyperparams, 2-Qubit hyperparams
{} validate python code snippet
{} add comments to jupyter notebook
{} validate jupyter notebook


# Custom Quantum Layer
## Introduction to CQ

Unlike traditional quantum layers, the CQ layer offers a high degree of customization, enabling the tailoring of the quantum circuit architecture to specific problem domains. This flexibility allows for the optimization of processing different patterns using quantum and classical neurons as needed, making the CQ layer particularly well-suited for applications such as quantum machine learning, quantum classification, physics-informed neural networks, and others. 

UNAVAILABLE: architecture, diagrams, reference from AR team's github pages for CQ Layer

## Key Benefits
- The primary advantage of the Custom Quantum layer is its ability to be highly configurable, allowing for the definition of the number of qubits, gate sets, and encoding methods that best suit the use case.
- The CQ layer provides a flexible interface for integrating quantum circuits into neural network architectures, enabling the harnessing of the power of quantum computing in a way that is optimized for specific problem domains.


## Hyperparameters and Default Settings
The following hyperparameters are included in the CQ layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter | Description                                                                                                                                                           | Syntax           | Range                             | Default           |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|-----------------------------------|-------------------|
| n_qubits       | Number of qubits in each quantum circuit. <br/>For best results, formulate `n_qubits` as a power of 2.                                                                | int              | 2 to 8                            | 4                 |
| n_qubits       | Number of qubits each gate acts on. <br/>For best results, formulate `n_qubits` as a power of 2.                                                                      | int              | 2 to 8                            | 4                 |
| gates          | A list of quantum gates, where each gate has its own set of parameters. The choice and order of gates determines the quantum operations performed on the input data. Can be `Pauli`, `Hadamard` or `CNOT`. | list of objects |   --    |                   |
| gates          | A list of quantum gates, where each gate has its own set of parameters. The choice and order of gates determines the quantum operations performed on the input data. Can be `Pauli`, `Hadamard` or `CNOT`. | list of objects |   --    |                   |


# 1-Qubit Gate Hyperparameters
| Hyperparameter | Description                                                                                                                                                                                                          | Syntax | Range    | Default  |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|----------|
| variational    | Controls the number of iterations for the quantum algorithm used to train the quantum layer. The variational algorithm optimizes the quantum circuit parameters to minimize a cost function.                         | int    | 1 to 100 | 12       |
| encoding       | Specifies the encoding method used to represent classical data in the quantum circuit. Different encoding techniques may be suitable for different types of problems. Can be `method1`, `method2` or `method3`.      | int    | 1 to 3   | 2        |
| measurement    | The number of measurements to perform on the quantum circuit. The measurement process collapses the quantum state and projects it onto a classical outcome. More measurements may provide more accurate results but may also increase noise and uncertainty.  | int    | 1 to 100 | 10 |
 qubits in each circuit will be measured. If set to 'None' each qubit will be measured  | str    | 'single', 'even', 'None' | 'None' |
| wire           | Specifies which qubit(s) a particular gate should be applied to. Indicates the qubit index.                                                                                                                          | int   | [0, n_qubits-1] | 0 |

# 2-Qubit Gate Hyperparameters
| Hyperparameter | Description                                                                                                                                                                                                      | Syntax | Range    | Default  |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|----------|----------|
| variational    | Controls the number of iterations for the quantum algorithm used to train the quantum layer. The variational algorithm optimizes the quantum circuit parameters to minimize a cost function.                     | int    | 1 to 100 | 12       |
| encoding       | Specifies the encoding method used to represent classical data in the quantum circuit. Different encoding techniques may be suitable for different types of problems. Can be `method1`, `method2` or `method3`.  | int    | 1 to 3   | 2        |
| measurement    | The number of measurements to perform on the quantum circuit. The measurement process collapses the quantum state and projects it onto a classical outcome. More measurements may provide more accurate results but may also increase noise and uncertainty.  | int    | 1 to 100 | 10 |
| wire           | Specifies which qubit(s) a particular gate should be applied to. Indicates the indices of the two qubits.                                                                                                        | int    | [0, n_qubits-1] | 0 |

## UNCLEAR : 
## 1. 3 definitions for measurement
## 2. Should I add entangling, measure and rotation to qubit gate hyperparams?

1. 3 defitions for measurement?
| measurement    | The number of measurements to perform on the quantum circuit. The measurement process collapses the quantum state and projects it onto a classical outcome. More measurements may provide more accurate results but may also increase noise and uncertainty.  | int    | 1 to 100 | 10 |
| measurement    | type of CNOTs configuration before measurement. When set to 'single', CNOTs would be applied at the end of each circuit and reduce the whole output dimension by :math:`ext{n_qubits}` times. If set to 'even' only 
| measure        | Pauli measurement that will be used at the end of each circuit. Can be `X`, `Y` or `Z`.                                    | str    | `X` `Y` `Z`                       | `Y`               |

2. Should I add entangling, measure and rotation to qubit gate hyperparams?

## USE THESE DESCRIPTIONS FOR QUBIT GATE HYPERPARAMS
| Gate Parameter | Description                                                                                                                | Syntax | Range    | Default  |
| entangling     | Type of entangling layer used. Can be `strong` or `basic`.                                                                 | str    | `strong` `basic`                  | `strong`          |
| measure        | Pauli measurement that will be used at the end of each circuit. Can be `X`, `Y` or `Z`.                                    | str    | `X` `Y` `Z`                       | `Y`               |
| rotation       | ADD DETAILED EXPLANATION. Type of embedding rotations used. Can be `X`, `Y` or `Z`.                                        | str    | `X` `Y` `Z`                       | `Z`               |

## Quantum Circuit Representation

UNAVAILBLE

## Sample Python Code Block

Here is an example of how to apply the custom quantum layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a custom quantum layer with a classical dense layer.

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
        data=DatasetStorageInfoProto(storage_id="47c6aba9-881b-4664-b714-dd9bb2f6bd5e")
    ),
)

with TQ42Client() as client:
    client.login()
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.GENERIC_ML_TRAIN,
        experiment_id="b2004690-2a4b-479e-bafe-13a475bb0d69",
        compute=HardwareProto.SMALL,
        parameters=MessageToDict(env_msg, preserving_proto_field_name=True)
    )

    print(run.data)

    result = run.poll()

    print(result.data)

```
