# Running Algorithms

There are four types of training algorithms, one for each model:

 - TS_MLP_TRAIN
 - TS_LSTM_TRAIN
 - TS_HQMLP_TRAIN
 - TS_HQLSTM_TRAIN

and four corresponding evaluation algorithms:

 - TS_MLP_EVAL
 - TS_LSTM_EVAL
 - TS_HQMLP_EVAL
 - TS_HQLSTM_EVAL

The appropriate parameters for each type of algorithm must be provided.

### Training Examples

The following example trains a classical MLP:

```python
from tq42.client import TQ42Client
from tq42.organization import list_all as list_all_organizations
from tq42.project import list_all as list_all_projects
from tq42.experiment import list_all as list_all_experiments
from tq42.experiment_run import ExperimentRun
from tq42.algorithm import (
    AlgorithmProto,
    DatasetStorageInfoProto,
    ActFuncProto,
    OptimProto,
    LossFuncProto,
    TSTrainInputsProto,
    TSMLPTrainMetadataProto,
    TSMLPTrainParametersProto
) 
from tq42.compute import HardwareProto

from google.protobuf.json_format import MessageToDict

params = MessageToDict(TSMLPTrainMetadataProto(
    parameters=TSMLPTrainParametersProto(
        input_width=24,
        label_width=1,
        dim_list=[60, 40, 30],
        act_func=ActFuncProto.RELU,
        dropout=False,
        dropout_p=0,
        bn=False,
        num_epochs=20,
        batch_size=128,
        learning_rate=0.001,
        optim=OptimProto.ADAM,
        loss_func=LossFuncProto.MAE,
    ),
    inputs=TSTrainInputsProto(
        data=DatasetStorageInfoProto(storage_id="random-uuid-with-training-data-inside")
    )
), preserving_proto_field_name=True)

with TQ42Client() as client:
    org_list = list_all_organizations(client=client)
    print(org_list)
    print("------------")
    org = org_list[0]
    proj_list = list_all_projects(client=client, organization_id=org.id)
    print("------------")
    print(proj_list)
    proj = proj_list[0]
    
    exp_list = list_all_experiments(client=client, project_id=proj.id)
    print(exp_list)
    
    print("running experiment for exp {}".format(exp_list[0]))
    
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.TS_MLP_TRAIN,
        experiment_id=exp_list[0].id,
        compute=HardwareProto.SMALL,
        parameters=params
    )
```

Further models can be trained by importing the relevant algorithm definition,

```python
from tq42.algorithm import TSLSTMTrainMetadataProto, TSHQMLPTrainMetadataProto, TSHQLSTMTrainMetadataProto 

TSLSTMTrainMetadataProto
TSHQMLPTrainMetadataProto
TSHQLSTMTrainMetadataProto
```

specifying the corresponding parameters (e.g.)

```python
from tq42.algorithm import (
    DatasetStorageInfoProto,
    ActFuncProto,
    OptimProto,
    LossFuncProto,
    TSTrainInputsProto,
    MeasureProto,
    MeasurementModeProto,
    EntanglingProto,
    DiffMethodProto,
    QubitTypeProto,
    TSLSTMTrainMetadataProto,
    TSLSTMTrainParametersProto
)

TSLSTMTrainMetadataProto(
    parameters=TSLSTMTrainParametersProto(
        input_width=24,
        label_width=1,
        hidden_size=17,
        dropout_coef=0.17,
        num_epochs=20,
        batch_size=128,
        learning_rate=0.001,
        optim=OptimProto.ADAM,
        loss_func=LossFuncProto.MAE,
    ),
    inputs=TSTrainInputsProto(
        data=DatasetStorageInfoProto(storage_id="random-uuid-with-training-data-inside")
    )
)

from tq42.algorithm import (
    TSHQMLPTrainMetadataProto,
    TSHQMLPTrainParametersProto
)

TSHQMLPTrainMetadataProto(
    parameters=TSHQMLPTrainParametersProto(
        input_width=1,
        label_width=1,
        hidden_size=10,
        num_qubits=2,
        depth=1,
        measurement_mode=MeasurementModeProto.NONE,
        rotation=MeasureProto.X,
        entangling=EntanglingProto.BASIC,
        measure=MeasureProto.Y,
        diff_method=DiffMethodProto.ADJOINT,
        qubit_type=QubitTypeProto.LIGHTNING_QUBIT,
        act_func=ActFuncProto.RELU,
        dropout=False,
        dropout_p=0.1,
        bn=False,
        num_epochs=5,
        batch_size=512,
        learning_rate=0.1,
        optim=OptimProto.ADAM,
        loss_func=LossFuncProto.MSE,
    ),
    inputs=TSTrainInputsProto(
        data=DatasetStorageInfoProto(storage_id="random-uuid-with-training-data-inside")
    )
)

from tq42.algorithm import (
    TSHQLSTMTrainMetadataProto,
    TSHQLSTMTrainParametersProto
)

TSHQLSTMTrainMetadataProto(
    parameters=TSHQLSTMTrainParametersProto(
        input_width=1,
        label_width=1,
        hidden_size=10,
        num_qubits=2,
        depth=1,
        n_qlayers=1,
        dropout_coef=0,
        num_epochs=5,
        batch_size=512,
        learning_rate=0.1,
        optim=OptimProto.ADAM,
        loss_func=LossFuncProto.MSE,
    ),
    inputs=TSTrainInputsProto(
        data=DatasetStorageInfoProto(storage_id="random-uuid-with-training-data-inside")
    )
)
```

and running the corresponding algorithm.

```python
from tq42.algorithm import AlgorithmProto

algorithm=AlgorithmProto.TS_LSTM_TRAIN
algorithm=AlgorithmProto.TS_HQMLP_TRAIN
algorithm=AlgorithmProto.TS_HQLSTM_TRAIN
```

### Evaluation Examples

The following example evaluates a classical MLP:

```python
from tq42.client import TQ42Client
from tq42.organization import list_all as list_all_organizations
from tq42.project import list_all as list_all_projects
from tq42.experiment import list_all as list_all_experiments
from tq42.experiment_run import ExperimentRun
from tq42.compute import HardwareProto
from tq42.algorithm import (
    AlgorithmProto,
    DatasetStorageInfoProto,
    ModelStorageInfoProto,
    TSEvalInputsProto,
    ActFuncProto,
    TSMLPEvalMetadataProto,
    TSMLPEvalParametersProto
) 

from google.protobuf.json_format import MessageToDict

params = MessageToDict(TSMLPEvalMetadataProto(
    parameters=TSMLPEvalParametersProto(
        input_width=24,
        label_width=1,
        dim_list=[60, 40, 30],
        act_func=ActFuncProto.RELU,
        dropout=False,
        dropout_p=0,
        bn=False
    ),
    inputs=TSEvalInputsProto(
        model=ModelStorageInfoProto(storage_id="MODEL_STORAGE_BUCKET_ID"),
        data=DatasetStorageInfoProto(storage_id="DATA_STORAGE_BUCKET_ID")
    )
), preserving_proto_field_name=True)

with TQ42Client() as client:
    org_list = list_all_organizations(client=client)
    print(org_list)
    print("------------")
    org = org_list[0]
    proj_list = list_all_projects(client=client, organization_id=org.id)
    print("------------")
    print(proj_list)
    proj = proj_list[0]
    
    exp_list = list_all_experiments(client=client, project_id=proj.id)
    print(exp_list)
    
    print("running experiment for exp {}".format(exp_list[0]))
    
    run = ExperimentRun.create(
        client=client,
        algorithm=AlgorithmProto.TS_MLP_EVAL,
        experiment_id=exp_list[0].id,
        compute=HardwareProto.SMALL,
        parameters=params
    )
```

Further models can be trained by importing the relevant algorithm definition,

```python
from tq42.algorithm import TSLSTMEvalMetadataProto, TSHQMLPEvalMetadataProto, TSHQLSTMEvalMetadataProto

TSLSTMEvalMetadataProto
TSHQMLPEvalMetadataProto
TSHQLSTMEvalMetadataProto
```

specifying the corresponding parameters (e.g.)

```python
from tq42.algorithm import (
    ModelStorageInfoProto,
    DatasetStorageInfoProto,
    TSEvalInputsProto,
    MeasurementModeProto,
    MeasureProto,
    EntanglingProto,
    ActFuncProto,
    DiffMethodProto,
    QubitTypeProto,
    TSLSTMEvalMetadataProto,
    TSLSTMEvalParametersProto
)

TSLSTMEvalMetadataProto(
    parameters=TSLSTMEvalParametersProto(
        input_width=24,
        label_width=1,
        hidden_size=17,
        dropout_coef=0.17
    ),
    inputs=TSEvalInputsProto(
        model=ModelStorageInfoProto(storage_id="MODEL_BUCKET_STORAGE_ID"),
        data=DatasetStorageInfoProto(storage_id="DATA_BUCKET_STORAGE_ID")
    )
)

from tq42.algorithm import (
    TSHQMLPEvalMetadataProto,
    TSHQMLPEvalParametersProto
)

TSHQMLPEvalMetadataProto(
    parameters=TSHQMLPEvalParametersProto(
        input_width=1,
        label_width=1,
        hidden_size=10,
        num_qubits=2,
        depth=1,
        measurement_mode=MeasurementModeProto.NONE,
        rotation=MeasureProto.X,
        entangling=EntanglingProto.BASIC,
        measure=MeasureProto.Y,
        diff_method=DiffMethodProto.ADJOINT,
        qubit_type=QubitTypeProto.LIGHTNING_QUBIT,
        act_func=ActFuncProto.RELU,
        dropout=False,
        dropout_p=0.1,
        bn=False,
    ),
    inputs=TSEvalInputsProto(
        model=ModelStorageInfoProto(storage_id="MODEL_BUCKET_STORAGE_ID"),
        data=DatasetStorageInfoProto(storage_id="DATA_BUCKET_STORAGE_ID")
    )  
)

from tq42.algorithm import (
    TSHQLSTMEvalMetadataProto,
    TSHQLSTMEvalParametersProto
)

TSHQLSTMEvalMetadataProto(
    parameters = TSHQLSTMEvalParametersProto(
        input_width=1,
        label_width=1,
        hidden_size=10,
        num_qubits=2,
        depth=1,
        n_qlayers=1,
        dropout_coef=0,      
    ),
    inputs=TSEvalInputsProto(
        model=ModelStorageInfoProto(storage_id="MODEL_BUCKET_STORAGE_ID"),
        data=DatasetStorageInfoProto(storage_id="DATA_BUCKET_STORAGE_ID")
    )  
)
```

and running the corresponding algorithm.

```python
from tq42.algorithm import AlgorithmProto

algorithm=AlgorithmProto.TS_LSTM_EVAL
algorithm=AlgorithmProto.TS_HQMLP_EVAL
algorithm=AlgorithmProto.TS_HQLSTM_EVAL
```
