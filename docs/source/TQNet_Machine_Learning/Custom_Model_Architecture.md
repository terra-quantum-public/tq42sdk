### Building a Custom Model with Layers
Build a custom model containing a mix of classical, hybrid, and quantum layers. Learn more about each layer below, and construct a custom model using any combination of layers you choose, defining hyperparameters for each.

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
        model_type=MLModelType.MLP,
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
        batch_size=128,
        learning_rate=0.01,
        optim=OptimProto.ADAM,
        loss_func=LossFuncProto.MAE,
        train_model_info=TrainModelInfoProto(
            # TODO: fill to better identify the trained model later on
            name="",
            description="",
        ),
    ),
    inputs=MLTrainInputsProto(
        # TODO: fill with your specific dataset storage id
        data=DatasetStorageInfoProto(storage_id="")
    ),
)

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.GENERIC_ML_TRAIN,
        # TODO: fill with your specific experiment id
        experiment_id="",
        compute=HardwareProto.SMALL,
        parameters=MessageToDict(metadata, preserving_proto_field_name=True)
    )

    print(run.data)

    result = run.poll()

    print(result.data)
```


