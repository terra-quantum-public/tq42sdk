# Create and list Datasets

## Create a Dataset

When you are ready to create a dataset, type `tq42 proj dataset create` and provide the following flags:
```bash
tq42 proj dataset create
    --proj="PROJ_ID"
    --name="DATASET_NAME"
    --desc="DESCRIPTION"
    --url="DATASET_URL"
    --sensitivity="DATASET_SENSITIVITY"
```

The preceding command consists of the xfollowing elements:

- `proj` is a `tq42` command group.

- `dataset` is an `proj` command group.

- `create` is a `dataset` command.

- `--proj` is a flag set to a project to which the dataset should be assigned.

- `--name` is the name of the newly created dataset.

- `--description` is the description of the newly created dataset.

- `--url` is the url for the newly created dataset. This is where the data is pulled from.

- `--sensitivity` is a flag set to indicate the sensitivity of the newly created dataset. Values are: PUBLIC, GENERAL, SENSITIVE, CONFIDENTIAL.

The output is just the id of the newly created dataset:

`<DATASET_ID>`

For example:
```bash
tq42 proj dataset create \ 
    --proj=5fd0f2cd-aa75-4ecb-924c-07270ed9cd32 \
    --name="cli_test_24-01-10" \
    --desc="cli_test_24-01-10" \
    --url="gs://tq-pvpower-demo-source" \
    --sensitivity=SENSITIVE

85a4c01b-1067-4852-bae4-b18d867664d5
```

## List Datasets

After you have created a dataset, the system will begin syncing the dataset. You can list all of your datasets by: 

```bash
tq42 proj dataset list --proj="PROJECT_ID" --type [DATASET] or [MODEL]
```

For example:
```bash
tq42 proj dataset list --proj="5fd0f2cd-aa75-4ecb-924c-07270ed9cd32" --type "MODEL"

[
id: "aff328cc-a5b4-4cac-80aa-370872e9dcb2"
name: "aff328cc-a5b4-4cac-80aa-370872e9dcb2"
created_at {
  seconds: 1704904788
  nanos: 109902000
}
status: DATASET_CREATED
progress: 100
, id: "c564d2c7-c891-4d5b-8cb0-b0bc511c14d5"
name: "c564d2c7-c891-4d5b-8cb0-b0bc511c14d5"
created_at {
  seconds: 1704905421
  nanos: 431659000
}
status: DATASET_CREATED
progress: 100
, id: "cf8520cc-15d2-4733-a6a7-16f0fcbbfd5c"
name: "cf8520cc-15d2-4733-a6a7-16f0fcbbfd5c"
created_at {
  seconds: 1704909327
  nanos: 558297000
}
status: DATASET_CREATED
progress: 100
]
```
