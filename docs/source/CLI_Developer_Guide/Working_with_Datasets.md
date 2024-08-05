# Working with Datasets

## Create a Dataset

When you are ready to create a dataset, type `tq42 proj dataset create` and provide the following flags:
```bash
tq42 proj dataset create
    --proj="PROJ_ID"
    --name="DATASET_NAME"
    --desc="DESCRIPTION"
    # either    
    --url="DATASET_URL"
    # or
    --file="LOCAL_FILE_PATH"
    --sensitivity="DATASET_SENSITIVITY"
```

The preceding command consists of the following elements:

- `proj` is a `tq42` command group.

- `dataset` is an `proj` command group.

- `create` is a `dataset` command.

- `--proj` is a flag set to a project to which the dataset should be assigned.

- `--name` is the name of the newly created dataset.

- `--description` is the description of the newly created dataset.

- `--url` is the url for the newly created dataset. This is where the data is pulled from.

- `--file` is the file path to upload to the newly created dataset. This is where the data is pulled from.

NOTE: Only choose one, url or file

- `--sensitivity` is a flag set to indicate the sensitivity of the newly created dataset. Values are: PUBLIC, GENERAL, SENSITIVE, CONFIDENTIAL.

The output is just the id of the newly created dataset.

## Get information about datasets

After you have created a dataset, the system will begin syncing the dataset.

You can do one of two things to get the status of this dataset (as well as others):

1. Get information about a specific dataset by running

```bash
tq42 proj dataset get <DATASET-ID>
```

2. You can list all of your datasets in a given project by running 

```bash
tq42 proj dataset list --proj="PROJECT_ID"
```

## Exporting a dataset

To make proper use of datasets an export functionality is key to extract data and leverage it for further workflows.
This can be achieved by running the following command

```bash
tq42 proj dataset export <DATASET_ID> <DIRECTORY_PATH_FOR_EXPORT>
```
