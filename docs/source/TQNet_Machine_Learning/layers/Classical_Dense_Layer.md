# Classical Dense Layer
## Introduction to Classical Dense
The Dense Layer, also known as the fully connected layer, is a fundamental building block in the architecture of many neural networks. Unlike convolutional layers that process input data in a local and spatially-invariant manner, the dense layer treats its input as a flat vector (hence, fully connected) and performs a linear transformation on it.

![Dense_Network_Layer_diagram.jpeg](../images/Dense_Network_Layer_diagram.jpeg)


## Key Benefits
- Dense layers are versatile and can be used in a wide range of neural network architectures, including feedforward neural networks, convolutional neural networks (CNNs), and recurrent neural networks (RNNs).
- Dense layers provide high expressive power, allowing the model to learn complex relationships between input features and target outputs. Each neuron in the layer is connected to every neuron in the previous and next layers, enabling the model to capture intricate patterns.
- The weights in a dense layer are trainable parameters that the neural network learns during training. This enables the model to automatically learn relevant features from the input data, reducing the need for manual feature engineering.
- Dense layers are typically followed by activation functions (e.g., ReLU, sigmoid, tanh), introducing non-linearity into the model. This helps the network learn and represent non-linear relationships in the data.
- The shared weights in a dense layer allow for parameter sharing, meaning that the same set of weights is applied to different input features. This can be beneficial for tasks where certain features should be treated similarly.
- Dense layers capture global dependencies in the data by considering interactions between all input features simultaneously. This makes them suitable for tasks where the relationship between input features is not locally confined.
- Dense layers are computationally straightforward and easy to implement. This simplicity makes them a go-to choice in many neural network architectures.
- The weights in a dense layer can provide insights into the importance of different features in the model. Analyzing the learned weights can offer some level of interpretability.

*Please note, the choice of neural network architecture and layer types depends on the specific requirements and characteristics of the task at hand. Different layer types, such as convolutional layers or recurrent layers, may be more suitable for certain types of data and tasks.

## Hyperparameters and Default Settings
The following hyperparameters are included in the Classical Dense layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter      | Description                                                   | Syntax | Range                 | Default         |
|---------------------|---------------------------------------------------------------|--------|-----------------------|-----------------|
| layers_dim          | Dimension of each `Classical Dense` layer.                    | int    | 1 to 5                | 2               |
| bias                | If set to `false`, the layer will not learn an additive bias. | bool   | `false` `true`        | `true`          |


## Sample Python Code Block
Here is an example of how to apply the Classical Dense layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single Classical Dense layer:

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
    ClassicalDenseLayer,
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
            Layer(classical_dense_layer=ClassicalDenseLayer(
                hidden_size=2,
                bias=True
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
