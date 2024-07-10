# Working with Models

## Get information about models

After an experiment run created a model, these models are available to query by the user.

To get the corresponding id you can query your experiment run like below and find the corresponding id 
(named `storageId`) in the `result` field under `outputs`.

```bash
tq42 exp run check <EXP-RUN-ID>
```

You can do one of two things to get the information about this specific model:

1. You can list all of your models in a given project by running 

```bash
tq42 proj model list --proj="PROJECT_ID"
```

2. Get information about a specific model by running

```bash
tq42 proj model get <MODEL-ID>
```
