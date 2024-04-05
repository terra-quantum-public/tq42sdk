# Dropout Layer
## Introduction to Dropout
Dropout is a regularization technique commonly used in machine learning and neural networks to prevent overfitting. Overfitting occurs when a model learns the training data too well, capturing noise and specific patterns that don't generalize well to new, unseen data. Dropout is a technique that helps mitigate overfitting by randomly dropping out (i.e., setting to zero) a fraction of the units or neurons in a neural network during training.

Dropout is typically applied during training and is turned off during inference (when making predictions). During inference, the full network is used, but the weights may be scaled to account for the dropout probability used during training.

Dropout has been successfully applied to various types of neural networks, including fully connected layers, convolutional layers, and recurrent layers, and it has become a standard technique for improving the generalization performance of machine learning models.

## How it Works
### During Training

At each training iteration, a random subset of neurons is selected to be "dropped out" or turned off. This means that the output of these neurons is set to zero.
The choice of which neurons to drop out is random and can vary for each training iteration. This introduces a form of randomness and prevents the network from relying too much on specific neurons.

### Variability

Dropout introduces variability into the training process, making the network less sensitive to the presence of any specific neuron. This helps prevent neurons from becoming overly specialized and encourages the network to learn more robust and general features.

### Ensemble Effect

Dropout can be viewed as training an ensemble of multiple models. In each training iteration, a different subset of neurons is active, effectively training different subnetworks. At test time, all neurons are active, but the weights are scaled to account for the dropout probability. This ensemble effect improves generalization performance.

### Regularization

Dropout acts as a form of regularization because it penalizes complex co-adaptations of neurons. The network is forced to be more robust and distribute learning across different sets of neurons.
The dropout rate is a hyperparameter that determines the probability of dropping out a neuron during training. Common dropout rates range from 0.2 to 0.5, but the optimal rate may vary depending on the specific task and dataset.


## Hyperparameters and Default Settings
The following hyperparameters are included in the Classical Dense layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter | Description                                                           | Syntax | Range  | Default |
|----------------|-----------------------------------------------------------------------|--------|--------|---------|
| `value`        | Probability of applying Dropout to the output features of each layer. | float  | 0 to 1 | 0.5     |


## Sample Python Code Block
Here is an example of how to apply the Dropout layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single Dropout layer:

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
    DropoutLayer,
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
            Layer(dropout_layer=DropoutLayer(
                value=0.5
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
