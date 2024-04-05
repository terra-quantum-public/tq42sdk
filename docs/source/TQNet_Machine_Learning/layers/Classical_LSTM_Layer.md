# Classical Long Short-Term Memory (LSTM) Layer
## Introduction to Classical Long Short-Term Memory (LSTM)
A classical Long Short-Term Memory (LSTM) layer is a type of recurrent neural network (RNN) layer designed to address the vanishing gradient problem and capture long-term dependencies in sequential data.


## Key Benefits
- LSTMs are specifically designed to address the issue of vanishing gradients in traditional RNNs, allowing them to capture dependencies in sequential data over longer time spans. This is particularly useful for tasks where understanding context over extended sequences is crucial.
- LSTMs incorporate memory cells that can store information for an extended period. These cells help the network remember important information and selectively update or forget certain parts of the memory based on the current input.
- LSTMs use gating mechanisms, including input gates, forget gates, and output gates. These gates regulate the flow of information into, out of, and within the memory cells. This enables the network to control the update and retention of information, enhancing its ability to capture relevant patterns.
- LSTMs facilitate better gradient flow during training, which helps in mitigating the vanishing gradient problem. The gating mechanisms allow the model to learn when to backpropagate errors through time, improving the training stability of the network.
- LSTMs can process sequential data in parallel to some extent, making them computationally more efficient than traditional RNNs. This is due to the fact that the memory cell's state can be updated independently of the input data, allowing for parallelization.
- LSTMs are well-suited for tasks involving sequential data, such as natural language processing (NLP), time series analysis, and speech recognition. They excel in capturing temporal dependencies and learning patterns in sequences of varying lengths.
- LSTMs can handle variable-length sequences, making them adaptable to tasks where input data may have different lengths. This is especially beneficial in applications like natural language processing, where sentences can vary in length.
- Pre-trained LSTM models on tasks like language modeling can be used as feature extractors for downstream tasks. The learned representations from the LSTM's hidden states can capture meaningful features in sequential data, aiding in transfer learning scenarios.
- The gating mechanisms in LSTMs allow them to selectively filter out noise and irrelevant information, making them more robust to noisy or irrelevant input data.


## Hyperparameters and Default Settings
The following hyperparameters are included in the Classical LSTM layer. These are not necessarily the recommended settings for every application or use case; they may require tuning to find the optimal values for your specific use case.

| Hyperparameter | Description                            | Syntax | Range      | Default |
|----------------|----------------------------------------|--------|------------|---------|
| hidden_size    | Size of the hidden classical vector.   | int    | 10 to 1000 | 17      |


## Sample Python Code Block
Here is an example of how to apply the Classical LSTM layer within a custom model architecture in the SDK.

The following example trains a custom time series prediction problem using a single Classical LSTM layer:

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
    ClassicalLSTMLayer,
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
            Layer(classical_lstm_layer=ClassicalLSTMLayer(
                hidden_size=17
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
