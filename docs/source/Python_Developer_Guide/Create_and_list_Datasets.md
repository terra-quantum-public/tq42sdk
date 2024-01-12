# Create and list Datasets

## Create a Dataset

hen you are ready to create a dataset, use the `Dataset` class and provide the following flags:

```python
from tq42.client import TQ42Client
from tq42.dataset import Dataset, DatasetSensitivityProto

with TQ42Client() as client:
    Dataset.create(
        client=client,
        project_id="PROJECT_ID",
        name="NAME",
        description="DESCRIPTION",
        url="BUCKET_URL",
        sensitivity=DatasetSensitivityProto.SENSITIVE
    )
```

The preceding command consists of the following elements:

- `project_id` is a flag set to a project to which the dataset should be assigned.

- `name` is the name of the newly created dataset. 

- `description` is the description of the newly created dataset.

- `url` is the url for the newly created dataset. This is where the data is pulled from.

- `sensitivity` is a flag set to indicate the sensitivity of the newly created dataset. Values can be found in the enum `DatasetSensitivityProto`.

The result of this dataset creation is a `Dataset` instance.

For example:

```python
from tq42.client import TQ42Client
from tq42.dataset import Dataset, DatasetSensitivityProto

with TQ42Client() as client:
    dataset = Dataset.create(
        client=client,
        name="testing_tshq_11_01_24",
        description="testing_tshq_11_01_24",
        url="gs://tq-pvpower-demo-source",
        sensitivity=DatasetSensitivityProto.SENSITIVE,
        project_id="cbbc8b76-146c-45b1-b70c-1a18eab29a07",
    )
```

## List Datasets

fter you have created a dataset, the system will begin syncing the dataset. You can list all of your datasets by:

```python
from tq42.client import TQ42Client
from tq42.dataset import list_all

with TQ42Client() as client:
    datasets = list_all(client=client, project_id="PROJECT_ID")
```

For example:

```python
from tq42.client import TQ42Client
from tq42.dataset import list_all

with TQ42Client() as client:
    datasets = list_all(client=client, project_id="cbbc8b76-146c-45b1-b70c-1a18eab29a07")
```
