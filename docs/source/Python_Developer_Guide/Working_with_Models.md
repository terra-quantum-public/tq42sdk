# Working with Models

## Get information about models

After an experiment run created a model, these models are available to query by the user.

To get the corresponding id you can query your experiment run like below and find the corresponding id 
(named `storageId`) in the `result` field under `outputs`.

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    exp_run = ExperimentRun(client=client, id="<YOUR_EXP_RUN_ID>")
    print(exp_run)
```

You can do one of two things to get the information about a model:

1. You can list all of your models in a given project by running

```python
from tq42.client import TQ42Client
from tq42.model import list_all

with TQ42Client() as client:
    models = list_all(client=client, project_id="<YOUR_PROJECT_ID>")
    print(models)
```

2. Get information about a specific model by running

```python
from tq42.client import TQ42Client
from tq42.model import Model

with TQ42Client() as client:
    model = Model(client=client, id="<YOUR_MODEL_ID>")
    print(model)
```