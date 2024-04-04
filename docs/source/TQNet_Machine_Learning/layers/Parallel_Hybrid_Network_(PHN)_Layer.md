# Parallel Hybrid Network (PHN) Layer
## Introduction to PHN
The Parallel Hybrid Network (PHN) layer consists of Quantum Depth Infused (QDI) and classical Linear layers. Due to the success of deep learning, where many layers of neurons are placed in a long sequence, the first attempts at designing hybrid neural networks involved arranging the quantum and classical layers sequentially. At Terra Quantum, we have pioneered the approach of putting the quantum layers in parallel with the classical ones.

[Reference](https://arxiv.org/pdf/2303.03227v1.pdf)

## Key Benefits
![PHN_Key_Benefits.jpg](../images/PHN_Key_Benefits.jpg)

## Hyperparameters and Default Settings
The following hyperparameters are included in the PHN layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter | Description                                                                                                                                                     | Syntax | Range                             | Default           |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------|-------------------|
| in_features    | Number of features in the data.                                                                                                                                 | int    | 1 to INT MAX                      |                   |
| n_qubits       | Number of qubits in each quantum circuit. <br/>Note that `in_features` must be divisible by `n_qubits`. For best results, formulate `n_qubits` as a power of 2. | int    | 2 to 8                            | 4                 |
| depth          | Number of variational layers inside one quantum circuit.                                                                                                        | int    | 1 to 8                            | 7                 |
| hidden_size    | Size of the hidden classical vector.                                                                                                                            | int    | 1 to 1000                         | 17                |
| rotation       | Type of embedding rotations used. Can be `X`, `Y` or `Z`.                                                                                                       | str    | `X` `Y` `Z`                       | `Z`               |
| entangling     | Type of entangling layer used. Can be `strong` or `basic`.                                                                                                      | str    | `strong` `basic`                  | `strong`          |
| measure        | Pauli measurement that will be used at the end of each circuit. Can be `X`, `Y` or `Z`.                                                                         | str    | `X` `Y` `Z`                       | `Y`               |
| diff_method    | Defines method for calculating gradients for quantum circuit. Must be either `adjoint` or `parameter-shift`.                                                    | str    | `adjoint` `parameter-shift`       | `adjoint`         |
| qubit_type     | Defines qubit device for simulating a quantum circuit. Must be either `lightning.qubit` or `lightning.gpu`.                                                     | str    | `lightning.qubit` `lightning.gpu` | `lightning.qubit` |


## Quantum Circuit Representation
This circuit diagram reflects the default settings listed above. To visualize a dynamic graph, please use the TQ42 web interface.

[Diagram coming soon]

## Sample Python Code Block
Here is an example of how to apply the PHN layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single PHN layer:

```python
from tq42.client import TQ42Client
from tq42.organization import list_all as list_all_organizations
from tq42.project import list_all as list_all_projects
from tq42.experiment import list_all as list_all_experiments
from tq42.experiment_run import ExperimentRun
from tq42.algorithm import (
    AlgorithmProto,
    DatasetStorageInfoProto,
    GenericMLTrainMetadataProto,
    GenericMLTrainParametersProto,
    Layer,
    MLTrainInputsProto,
    PHNLayer,
    MeasureProto,
    EntanglingProto,
    DiffMethodProto,
    QubitTypeProto,
)
from tq42.compute import HardwareProto

from google.protobuf.json_format import MessageToDict


params = MessageToDict(GenericMLTrainMetadataProto(
    parameters=GenericMLTrainParametersProto(
        # ... TODO: add the other parameters of your choice
        layers=[
            Layer(phn_layer=PHNLayer(
                in_features=20,
                num_qubits=4,
                depth=4,
                hidden_size=40,
                rotation=MeasureProto.Z,
                entangling=EntanglingProto.STRONG,
                measure=MeasureProto.Y,
                diff_method=DiffMethodProto.ADJOINT,
                qubit_type=QubitTypeProto.LIGHTNING_QUBIT)
            )
        ],
    ),
    inputs=MLTrainInputsProto(
        data=DatasetStorageInfoProto(storage_id="random-uuid-with-training-data-inside")
    )
), preserving_proto_field_name=True)

with TQ42Client() as client:
    org_list = list_all_organizations(client=client)
    org = org_list[0]
    proj_list = list_all_projects(client=client, organization_id=org.id)
    proj = proj_list[0]

    exp_list = list_all_experiments(client=client, project_id=proj.id)

    print("running experiment for exp {}".format(exp_list[0]))

    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.GENERIC_ML_TRAIN,
        exp=exp_list[0].id,
        compute=HardwareProto.SMALL,
        parameters=params
    )
```
