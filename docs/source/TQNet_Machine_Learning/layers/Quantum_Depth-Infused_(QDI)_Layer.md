# Quantum Depth-Infused (QDI) Layer
## Introduction to QDI
Rather than encoding each feature on a separate qubit, which would require an unrealistic number of qubits and be highly susceptible to the noise-rich barren plateau problem, we employ a data re-uploading method to create a lattice of features. The use of variational layers, entangling gates, and angle encoding allows the model to transform and entangle the data in a way that it can represent complex patterns and correlations in the data, offering better expressiveness.

![QDI layer architecture](../images/QDI_layer_architecture.png)

[Reference](https://www.mdpi.com/2072-6694/15/10/2705)

## Key Benefits
- The advantage of this approach is its efficient use of available qubits to handle a large amount of data, especially considering current technological constraints. By using a lattice structure and the data re-uploading method, one can encode a large number of features (for example, 256) into a manageable number of qubits (for example, 8).
- This not only enables the handling of large datasets but also mitigates the barren plateau problem, which could render the model impossible to train.

## Hyperparameters and Default Settings
The following hyperparameters are included in the QDI layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter   | Description                                                                                                                                                                                                                                                                                                                   | Syntax | Range                             | Default           |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-----------------------------------|-------------------|
| n_qubits         | Number of qubits in each quantum circuit. <br/>Note that `in_features` must be divisible by `n_qubits`. For best results, formulate `n_qubits` as a power of 2.                                                                                                                                                               | int    | 1 to 25                           | 4                 |
| depth            | Number of variational layers inside one quantum circuit.                                                                                                                                                                                                                                                                      | int    | 1 to 30                           | 4                 |
| measurement_mode | Type of CNOTs configuration before measurement. <br/>When set to `single`, CNOTs would be applied at the end of each circuit and reduce the whole output dimension by `n_qubits` times. <br/>If set to `even` only (0, 2, 4, ...) qubits in each circuit will be measured. <br/>If set to `none` each qubit will be measured. | str    | `single` `even` `none`            | `none`            |
| rotation         | Type of embedding rotations used. Can be `X`, `Y` or `Z`.                                                                                                                                                                                                                                                                     | str    | `X` `Y` `Z`                       | `Z`               |
| entangling       | Type of entangling layer used. Can be `strong` or `basic`.                                                                                                                                                                                                                                                                    | str    | `strong` `basic`                  | `strong`          |
| measure          | Pauli measurement that will be used at the end of each circuit. Can be `X`, `Y` or `Z`.                                                                                                                                                                                                                                       | str    | `X` `Y` `Z`                       | `Y`               |
| diff_method      | Defines method for calculating gradients for quantum circuit. Must be either `adjoint` or `parameter-shift`.                                                                                                                                                                                                                  | str    | `adjoint` `parameter-shift`       | `adjoint`         |
| qubit_type       | Defines qubit device for simulating a quantum circuit. Must be either `lightning.qubit` or `lightning.gpu`.                                                                                                                                                                                                                   | str    | `lightning.qubit` `lightning.gpu` | `lightning.qubit` |


## Quantum Circuit Representation
This circuit diagram reflects the default settings listed above, plus 12 input features. To visualize a dynamic graph, please use the TQ42 web interface.

![QDI Circuit Diagram](../images/QDI_Circuit_Diagram.png)


## Sample Python Code Block
Here is an example of how to apply the QDI layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single QDI layer:

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
    QDILayer,
    MeasureProto,
    EntanglingProto,
    DiffMethodProto,
    QubitTypeProto,
    MeasurementModeProto
)
from tq42.compute import HardwareProto

from google.protobuf.json_format import MessageToDict


params = MessageToDict(GenericMLTrainMetadataProto(
    parameters=GenericMLTrainParametersProto(
        # You may add and customize as many layers as you like
        layers=[
            Layer(qdi_layer=QDILayer(in_features=20,
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
