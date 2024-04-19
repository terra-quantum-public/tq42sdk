# Setting Up Your Environment

## Check Your Current Organization and Project Settings

Since users may belong to multiple organizations, or may be a member of several projects (each with their own budgets), before running an experiment it is important to check that you are working within the correct organization and project. 

To check your current organization and project, use:

```python
from tq42.client import TQ42Client
from tq42.project import Project

with TQ42Client() as client:
    Project.show(client=client)
```


## List All Organizations

To list all the organizations you have permission to view, use `list_all` provided by the `tq42.organization` module.
The system will return a list of orgs you have permission to view.

For example:
```python
from tq42.client import TQ42Client
from tq42.organization import list_all

with TQ42Client() as client:
    list_all(client=client)
```


## List All Projects

To list all the projects you have permission to view within a specific organization, use:
```python
from tq42.client import TQ42Client
from tq42.project import list_all

with TQ42Client() as client:
    list_all(client=client, organization_id="ORG_ID")
```

The system will return a list of available projects instances belonging to the organization associated with the `ORG_ID`.


## List All Experiments

To list all the experiments you have permission to view within a specific project, type:

```python
from tq42.experiment import list_all
from tq42.client import TQ42Client

with TQ42Client() as client:
    list_all(client=client, project_id="PROJ_ID")
```

The system will return a list of available experiments instances.


## List All Runs within an Experiment

To list all the runs within an experiment you have permission to view,
use the list_all function in `tq42.experiment_run`:

```python
from tq42.experiment_run import list_all
from tq42.client import TQ42Client

with TQ42Client() as client:
    list_all(client=client, experiment_id="EXP_ID")
```

The system will return a list of ExperimentRun instances within the specified experiment associated with the `EXP_ID`.

## Changing Your Workspace to a Different Organization or Project

To change the organization you are working within, use the `set` method on an `Organization` instance
The system will change the active organization and confirm the org ID.
The system will also return the default project ID for that organization,
so you know which project you are currently working within by default.

For example:
```python
from tq42.client import TQ42Client
from tq42.organization import Organization

with TQ42Client() as client:
    Organization(client=client, id="ORG_ID").set()
```

To change only the project, use:
```python
from tq42.client import TQ42Client
from tq42.project import Project

with TQ42Client() as client:
    Project(client=client, id="PROJ_ID").set()
```

The system will change the active project and confirm the org ID as well as the project ID.

## Setting Friendly Names for Projects and Experiments

The ID strings for Projects and Experiments can be difficult to navigate due to their length and complexity. To make it easier to reference, you can set a friendly name for Projects and Experiments from the CLI or Python tools, or from the TQ42 user interface. Note: updating the friendly names for a Project or Experiment in one place will update it everywhere, and will be visible to all team members who have access to that Project or Experiment. It is not possible to set a friendly name for an organization.

To set a friendly name for a project, so it is easier to reference than the `PROJ_ID` string, use:
```python
from tq42.client import TQ42Client
from tq42.project import Project

with TQ42Client() as client:
    Project(client=client, id="23e9715e-6f0e-4819-b9f2-88db9ef0a599").set_friendly_name(friendly_name="Fleet Routing")
```

The system will change the friendly name for that project and automatically return the friendly name value, so you can confirm it.

To set a friendly name for an experiment, so it is easier to reference than the `EXP_ID` string, type:
```python
from tq42.client import TQ42Client
from tq42.experiment import Experiment

with TQ42Client() as client:
    Experiment(client=client, id="EXP_ID").set_friendly_name(friendly_name="friendly name")
```

The system will change the friendly name for that experiment and return the experiment instance itself.

## Creating a Dataset and Listing Datasets

You can create a dataset for an experiment 

The API call to create a dataset needs the following arguments:
        client: TQ42Client,
        project_id: str,
        name: str,
        description: str,
        url: str,
        sensitivity: str,

```python
from tq42.client import TQ42Client
from tq42.dataset import Dataset, DatasetSensitivityProto

with TQ42Client() as client:
    Dataset.create(client=client, project_id="PROJ_ID", name="Dataset Name", description="Dataset description", url="https://dataset.url/data", sensitivity=DatasetSensitivityProto.CONFIDENTIAL),
```
You can list all datasets for a project by running:

```python
from tq42.client import TQ42Client
from tq42.dataset import list_all

with TQ42Client() as client:
    list_all(client=client, project_id="PROJ_ID")
```