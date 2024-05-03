# Setting Up Your Environment

## Check Your Current Organization and Project Settings

Since users may belong to multiple organizations, or may be a member of several projects (each with their own budgets), before running an experiment it is important to check that you are working within the correct organization and project. 

To check your current organization and project, use:

```python
from tq42.client import TQ42Client
from tq42.project import Project

with TQ42Client() as client:
    current_project = Project.show(client=client)
    print(current_project)
```


## List All Organizations

To list all the organizations you have permission to view, use `list_all` provided by the `tq42.organization` module.
The system will return a list of orgs you have permission to view.

For example:
```python
from tq42.client import TQ42Client
from tq42.organization import list_all

with TQ42Client() as client:
    organizations = list_all(client=client)
    print(organizations)
```


## List All Projects

To list all the projects you have permission to view within a specific organization, use:
```python
from tq42.client import TQ42Client
from tq42.project import list_all

with TQ42Client() as client:
    projects = list_all(client=client, organization_id="<YOUR_ORG_ID>")
    print(projects)
```

The system will return a list of available projects instances belonging to the organization associated with the `ORG_ID`.


## List All Experiments

To list all the experiments you have permission to view within a specific project, type:

```python
from tq42.experiment import list_all
from tq42.client import TQ42Client

with TQ42Client() as client:
    experiments = list_all(client=client, project_id="<YOUR_PROJ_ID>")
    print(experiments)
```

The system will return a list of available experiments instances.


## List All Runs within an Experiment

To list all the runs within an experiment you have permission to view,
use the `list_all` function in `tq42.experiment_run`:

```python
from tq42.experiment_run import list_all
from tq42.client import TQ42Client

with TQ42Client() as client:
    experiment_runs = list_all(client=client, experiment_id="<YOUR_EXP_ID>")
    print(experiment_runs)
```

The system will return a list of ExperimentRun instances within the specified experiment associated with the `EXP_ID`.

## Changing Your Workspace to a Different Organization or Project

To change the organization you are working within, use the `set` method on an `Organization` instance
The system will change the active organization and return the organization instance.
You can verify the correct id by printing it.
The system will also try to set a default project ID for that organization.

For example:
```python
from tq42.client import TQ42Client
from tq42.organization import Organization
from tq42.project import Project

with TQ42Client() as client:
    organization = Organization(client=client, id="<YOUR_ORG_ID>").set()
    print(f"Default organization set to {organization.id}")
    project = Project.show()
    print(f"Default project set to {project.id}")
    
```

To change only the project, use:
```python
from tq42.client import TQ42Client
from tq42.project import Project

with TQ42Client() as client:
    project = Project(client=client, id="<YOUR_PROJ_ID>").set()
    print(f"Default project set to {project.id}")
```

The system will change the active project and return an instance of the default project.

## Setting Friendly Names for Projects and Experiments

The ID strings for Projects and Experiments can be difficult to navigate due to their length and complexity.
To make it easier to reference, you can set a friendly name for Projects and Experiments from the CLI or Python tools,
or from the TQ42 user interface. Note: updating the friendly names for a Project or Experiment in one place will update it everywhere, and will be visible to all team members who have access to that Project or Experiment.
It is not possible to set a friendly name for an organization.

To set a friendly name for a project, so it is easier to reference than the `PROJ_ID` string, use:
```python
from tq42.client import TQ42Client
from tq42.project import Project

with TQ42Client() as client:
    project = Project(client=client, id="<YOUR_PROJ_ID>").set_friendly_name(friendly_name="Fleet Routing")
    print(project)
```

The system will change the friendly name for that project and return the updated instance of this project.

To set a friendly name for an experiment, so it is easier to reference than the `EXP_ID` string, type:
```python
from tq42.client import TQ42Client
from tq42.experiment import Experiment

with TQ42Client() as client:
    experiment = Experiment(client=client, id="<YOUR_EXP_ID>").set_friendly_name(friendly_name="friendly name")
    print(experiment)
```

The system will change the friendly name for that experiment and return the updated experiment instance itself.

## Creating a Dataset and Listing Datasets

You can create a dataset for an experiment 

The API call to create a dataset needs the following arguments:
- client: TQ42Client
- project_id: str
- name: str
- description: str
- url: str
- sensitivity: str

```python
from tq42.client import TQ42Client
from tq42.dataset import Dataset, DatasetSensitivityProto

with TQ42Client() as client:
    dataset = Dataset.create(
        client=client,
        project_id="<YOUR_PROJ_ID>",
        name="Dataset Name", 
        description="Dataset description",
        url="https://dataset.url/data", 
        sensitivity=DatasetSensitivityProto.CONFIDENTIAL
    )
    print(dataset)
```
You can list all datasets for a project by running:

```python
from tq42.client import TQ42Client
from tq42.dataset import list_all

with TQ42Client() as client:
    datasets = list_all(client=client, project_id="<YOUR_PROJ_ID>")
    print(datasets)
```