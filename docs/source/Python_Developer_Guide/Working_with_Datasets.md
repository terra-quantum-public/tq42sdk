# Working with Datasets

## Create a Dataset

When you are ready to create a dataset, use the `Dataset` class and provide the following flags:

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


## Get information about datasets

After you have created a dataset, the system will begin syncing the dataset.

You can do one of two things to get the status of this dataset (as well as others):

1. Get information about a specific dataset by running

```python
from tq42.client import TQ42Client
from tq42.dataset import Dataset

with TQ42Client() as client:
    dataset = Dataset(client=client, id="<YOUR_DATASET_ID>")
    print(dataset)
```

2. You can list all of your datasets in a given project by running 

```python
from tq42.client import TQ42Client
from tq42.dataset import list_all

with TQ42Client() as client:
    datasets = list_all(client=client, project_id="<YOUR_PROJECT_ID>")
    print(datasets)
```

## Exporting a dataset

To make proper use of datasets an export functionality is key to extract data and leverage it for further workflows.
This can be achieved by running the following command

```python
from tq42.client import TQ42Client
from tq42.dataset import Dataset

with TQ42Client() as client:
    dataset = Dataset(client=client, id="<YOUR_DATASET_ID>")
    print(dataset)
    exported_files = dataset.export(directory_path="<YOUR_EXPORT_PATH>")
    print(exported_files)
```