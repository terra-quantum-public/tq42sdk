# Exponential Fourier Quantum (EFQ) Layer
## Introduction to EFQ
Fourier analysis enables general functions to be approximated by sums of trigonometric functions. Certain quantum encodings can create an asymptotically universal Fourier estimator. That is, a long enough sequences of quantum gates can fit any given function arbitrarily precisely. In our architecture, the Fourier degree grows exponentially.

![EFQ layer architecture](../images/EFQ_layer_architecture.png)

[Reference](https://arxiv.org/pdf/2212.00736.pdf)

## Key Benefits
- The main benefit of our exponential quantum encoding is that it creates a better Fourier estimator using fewer quantum gates.


## Hyperparameters and Default Settings
The following hyperparameters are included in the EFQ layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter   | Description                                                                                                                                                                                                                                                                                                                   | Syntax | Range                             | Default           |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------|-------------------|
| n_qubits         | Number of qubits in each quantum circuit. <br/>Note that `in_features` must be divisible by `n_qubits`. For best results, formulate `n_qubits` as a power of 2.                                                                                                                                                               | int    | 1 to 25                           | 4                 |
| depth            | Number of variational layers inside one embedding layer.                                                                                                                                                                                                                                                                      | int    | 1 to 30                           | 4                 |
| measurement_mode | Type of CNOTs configuration before measurement. <br/>When set to `single`, CNOTs would be applied at the end of each circuit and reduce the whole output dimension by `n_qubits` times. <br/>If set to `even` only (0, 2, 4, ...) qubits in each circuit will be measured. <br/>If set to `none` each qubit will be measured. | str    | `single` `even` `none`            | `none`            |
| rotation         | Type of embedding rotations used. Can be `X`, `Y` or `Z`.                                                                                                                                                                                                                                                                     | str    | `X` `Y` `Z`                       | `Z`               |
| entangling       | Type of entangling layer used. Can be `strong` or `basic`.                                                                                                                                                                                                                                                                    | str    | `strong` `basic`                  | `strong`          |
| measure          | Pauli measurement that will be used at the end of each circuit. Can be `X`, `Y` or `Z`.                                                                                                                                                                                                                                       | str    | `X` `Y` `Z`                       | `Y`               |
| diff_method      | Defines method for calculating gradients for quantum circuit. Must be either `adjoint` or `parameter-shift`.                                                                                                                                                                                                                  | str    | `adjoint` `parameter-shift`       | `adjoint`         |
| qubit_type       | Defines qubit device for simulating a quantum circuit. Must be either `lightning.qubit` or `lightning.gpu`.                                                                                                                                                                                                                   | str    | `lightning.qubit` `lightning.gpu` | `lightning.qubit` |


## Quantum Circuit Representation
This circuit diagram reflects the default settings listed above, plus 12 input features. To visualize a dynamic graph, please use the TQ42 web interface.

![EFQ Circuit Diagram](../images/EFQ_Circuit_Diagram.png)

## Sample Python Code Block
Here is an example of how to apply the EFQ layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single EFQ layer:

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
    EFQLayer,
    MeasureProto,
    EntanglingProto,
    DiffMethodProto,
    QubitTypeProto,
    MeasurementModeProto,
)
from tq42.compute import HardwareProto

from google.protobuf.json_format import MessageToDict


params = MessageToDict(GenericMLTrainMetadataProto(
    parameters=GenericMLTrainParametersProto(
        # Choose model type here
        model_type=MLModelType.MLP,
        # Add and customize and customize layers here
        layers=[
            Layer(efq_layer=EFQLayer(in_features=20,
               num_qubits=4,
               depth=4,
               measurement_mode = MeasurementModeProto.NONE,
               rotation=MeasureProto.Z,
               entangling=EntanglingProto.STRONG,
               measure=MeasureProto.Y,
               diff_method=DiffMethodProto.ADJOINT,
               qubit_type=QubitTypeProto.LIGHTNING_QUBIT
            ))
        ],
    ),
    inputs=MLTrainInputsProto(
        # Provide the specific dataset storage ID of the data you uploaded to TQ42.
        data=DatasetStorageInfoProto(storage_id="ENTER_DATASET_STORAGE_ID_HERE")
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
