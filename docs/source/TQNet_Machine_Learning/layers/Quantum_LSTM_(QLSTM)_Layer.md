# Quantum Long Short-Term Memory (QLSTM) Layer
## Introduction to Quantum Long Short-Term Memory (QLSTM)
Long short-term memory is a type of recurrent neural network. It handles data that is sequential (e.g., temporal) and has applications in places such as natural language processing and time series prediction. The quantum analog of this recurrent neural network is more expressive, allowing one to find more complex patterns in the data, which leads to an increase in the accuracy of model predictions.

![QLSTM layer architecture.png](../images/QLSTM_layer_architecture.png)

## Key Benefits
- It may converge faster and more precise predictions than purely classical Long Short-Term Memory Networks.


## Hyperparameters and Default Settings
The following hyperparameters are included in the Quantum LSTM layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter | Description                                                                                                                | Syntax | Range           | Default |
|----------------|----------------------------------------------------------------------------------------------------------------------------|--------|-----------------|---------|
| hidden_size    | This is the number of features in the hidden state h.                                                                      | int    | 10 to 1000      | 17      |
| n_qubits       | Number of qubits in each quantum circuit. <br/>For best results, formulate `n_qubits` as a power of 2.                     | int    | 1 to 25         | 4       |
| n_qlayers      | Number of entangling layers repetitions.                                                                                   | int    | 1 to 5          | 1       |
| depth          | Number of variational layers inside one quantum circuit.                                                                   | int    | 1 to 30         | 1       |
| batch_first    | If ``True``, then the input and output tensors are provided as `(batch, seq, feature)` instead of `(seq, batch, feature)`. | bool   | `true` `false`  | `false` |
| bidirectional  | If ``True``, becomes a bidirectional QLSTM.                                                                                | bool   | `true` `false`  | `false` |
| inversward     | If True, then the sequence of input data is read by the QLSTM layer in inverse order.                                      | bool   | `true` `false`  | `false` |


## Sample Python Code Block
Here is an example of how to apply the Quantum LSTM layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single Quantum LSTM layer:

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
    QLSTMLayer,
    MLTrainInputsProto,
)
from tq42.compute import HardwareProto

from google.protobuf.json_format import MessageToDict


params = MessageToDict(GenericMLTrainMetadataProto(
    parameters=GenericMLTrainParametersProto(
        # Choose model type here
        model_type=MLModelType.MLP,
        # Add and customize and customize layers here
        layers=[
            Layer(qlstm_layer=QLSTMLayer(
                hidden_size=17,
                num_qubits=4,
                num_qlayers=1,
                depth=1,
                bidirectional=False,
                inversward=False
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
```
