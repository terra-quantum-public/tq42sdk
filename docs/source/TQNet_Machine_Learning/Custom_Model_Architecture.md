### Building a Custom Model with Layers
Build a custom model containing a mix of classical, hybrid, and quantum layers. Learn more about each layer below, and construct a custom model using any combination of layers you choose, definining parameters and inputs for each.

See below for an example:

```python
from google.protobuf.json_format import MessageToDict

from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.algorithm import (
    GenericMLTrainMetadataProto,
    GenericMLTrainParametersProto,
    MLModelType,
    Layer,
    ClassicalDenseLayer,
    ActivationFunctionLayer,
    ActFuncProto,
    DropoutLayer,
    BatchNormalizationLayer,
    OptimProto,
    LossFuncProto,
    TrainModelInfoProto,
    MLTrainInputsProto,
    DatasetStorageInfoProto,
    AlgorithmProto,
)
from tq42.compute import HardwareProto

metadata = GenericMLTrainMetadataProto(
    parameters=GenericMLTrainParametersProto(
        # Choose model type here
        model_type=MLModelType.MLP,
        # Add and customize and customize layers here
        layers=[
            Layer(classical_dense_layer=ClassicalDenseLayer(hidden_size=4, bias=True)),
            Layer(classical_dense_layer=ClassicalDenseLayer(hidden_size=4, bias=True)),
            Layer(
                activation_function_layer=ActivationFunctionLayer(
                    function=ActFuncProto.RELU
                )
            ),
            Layer(dropout_layer=DropoutLayer(value=0.1)),
            Layer(batch_normalization_layer=BatchNormalizationLayer()),
            Layer(classical_dense_layer=ClassicalDenseLayer(hidden_size=4, bias=False)),
            Layer(classical_dense_layer=ClassicalDenseLayer(hidden_size=1, bias=False)),
        ],
        num_epochs=5,
        k_fold=1,
        batch_size=128,
        learning_rate=0.01,
        optim=OptimProto.ADAM,
        loss_func=LossFuncProto.MAE,
        train_model_info = TrainModelInfoProto(
            # Provide a unique name to identify your trained model.
            name="ENTER_MODEL_NAME_HERE",
            # Add a brief description to help users understand the purpose or functionality of this trained model.
            description="ADD_DESCRIPTION_HERE",
        ),
    ),
    inputs = MLTrainInputsProto(
        # Provide the specific dataset storage ID of the data you uploaded to TQ42.
        data=DatasetStorageInfoProto(storage_id="ENTER_DATASET_STORAGE_ID_HERE")
    ),
)

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.GENERIC_ML_TRAIN,
        # Fill in with the specific ID of the experiment you created in TQ42.
        experiment_id="ENTER_EXPERIMENT_ID_HERE",
        compute=HardwareProto.SMALL,
        parameters=MessageToDict(metadata, preserving_proto_field_name=True)
    )

    print(run.data)

    result = run.poll()

    print(result.data)
```

Explanation of the user configurable variables.

| Variable           | Explanation                                                                                     | Options                 |
|--------------------|-------------------------------------------------------------------------------------------------|-------------------------|
| `model_type`         | Specifies the type of machine learning model to be trained.                                    | MLP (Multi-layer Perceptron) `MLModelType.MLP` <br> RNN (Recurrent Neural Network) `MLModelType.RNN` |
| `layers`             | List of layers to be included in the model architecture. Each layer can be classical or quantum.| Refer to the next section for the available layers            |
| `num_epochs`         | Number of epochs (iterations over the entire dataset) to train the model.                       | Integer value greater than 0                              |
| `batch_size`         | Number of samples per gradient update.                                                         | Integer value greater than 0                              |
| `learning_rate`      | Learning rate determines the step size at each iteration while moving toward a minimum of the loss function. | Float value greater than 0                  |
| `optim`              | Optimization algorithm to be used during training.                                             | ADAM (Adaptive Moment Estimation) `OptimProto.ADAM` <br> ADAMW (Adam with weight decay) `OptimProto.ADAMW` <br> SGD (Stochastic Gradient Descent) `OptimProto.SGD` |
| `loss_func`          | Loss function to be minimized during training.                                                  | MAE (Mean Absolute Error) `LossFuncProto.MAE` <br> MSE (Mean Squared Error) `LossFuncProto.MSE`  <br> BCE (Binary Cross-Entropy) `LossFuncProto.BCE` <br> Cross-Entropy loss function `LossFuncProto.CROSSENTROPY` |
| `train_model_info`  | Information to better identify the trained model later on.                                      | Plaintext name and description of the model provided by the user |
|                     |                                                                                                 |                                                            |
| `inputs`             | Data input configuration specifying the dataset storage information.                            |                                                           |
| `data`               | The dataset used for training.                                                                  |                                                           |
| `storage_id`         | Identifier for the training dataset.                                                            | String representing the dataset storage location provided by the user |
|                      |                                                                                                 |                                                        |
| `experiment_id`      | String representing the experiment ID. Can be seen after the user creates an experiment in TQ42.| Provided by user                                      |
| `compute`            | Hardware configuration for the training process.                                                | `HardwareProto.SMALL` <br> `HardwareProto.MEDIUM` <br> `HardwareProto.LARGE` <br> `HardwareProto.SMALL_GPU` <br> `HardwareProto.MEDIUM_GPU` <br> `HardwareProto.LARGE_GPU` |
