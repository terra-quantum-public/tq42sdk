![](images/TQ42_Logo_Black_Teal.svg)

# Introduction to TQ42
The TQ42 Python SDK puts the power in your hands to accelerate delivery of custom, high-impact solutions. After installing the SDK and authenticating, access algorithms such as TetraOpt – a global optimization library based on tensor train (TT) decomposition. 

With TQ42, there is no need to build or manage your own quantum circuits. Let our algorithms do the work. From the CLI or a Jupyter notebook:

- Specify your objective function, hyper parameters, and compute infrastructure
- Run and manage experiments
- Visualize results

Collaborate with your teams across organizations and projects, and visit tq42.com for web-based tools to help you manage your account, projects, and experiments.

# TQ42 Features

![](images/TQ42-README-features-Infographic.jpg)

# Getting Started
## System Requirements
Be sure your system can support TQ42, which requires the following:
- Any modern operating system, in particular, Mac OSX 12.0 (Ventura) or above, Windows 10+, Linux will do
- Python 3.8 or above
- x86 64-bit CPU (Intel / AMD architecture); ARM CPUs are not supported
- 4 GB RAM
- 5 GB free disk space

The following Python packages are hard dependencies, and will automatically be installed alongside TQ42:
- [protobuf](https://googleapis.dev/python/protobuf/latest/)
- [grpcio-tools](https://pypi.org/project/grpcio-tools/) 


## Installation
Prior to installing TQ42, create a virtual environment or conda environment.
- [virtual environment](https://docs.python.org/3/library/venv.html)
- [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

TQ42 is published on pypi, so on x86_64, i686, ppc64le, s390x, and aarch64 Linux systems, x86_64 on Mac OSX, and 32 and 64 bit Windows installing is as simple as running the `pip install tq42` command:
```bash
pip install tq42
```

NOTE: We will refer to `pip` rather than `pip3`. Depending on how your system is configured you may have to use `pip3` rather than `pip` if the alias is not set.


## Authentication
After installing TQ42, authenticate by typing the `tq42 auth login` CLI command:
```bash
tq42 auth login
```

Or use the Python command:

```python
from tq42.client import TQ42Client

with TQ42Client() as client:
    client.login()
```

This command will open a window in your browser where you must enter your TQ42 username and password to authenticate.

If you have previously authenticated and your credentials are still valid, you will be automatically authenticated. However, if your credentials have expired, you will see a prompt to authenticate and can re-authenticate using the command above.

## Create an exemplary experiment run

After a successful login the next step is to create an experiment run.
A created experiment is necessary for this to work. This can be done via the Web UI.

To supply the experiment run the id of the created experiment is necessary.
This can be either retrieved by the UI or, alternatively, can be queried via the TQ42 Python SDK like this:

```python
from tq42.client import TQ42Client
from tq42.organization import list_all as list_all_organizations
from tq42.project import list_all as list_all_projects
from tq42.experiment import list_all as list_all_experiments

with TQ42Client() as client:
    client.login()
    org_list = list_all_organizations(client=client)
    # gets the first organization we can find
    org = org_list[0]
    proj_list = list_all_projects(client=client, organization_id=org.id)
    # gets the first project we can find
    proj = proj_list[0]
    exp_list = list_all_experiments(client=client, project_id=proj.id)
    # gets the id for the first experiment we can find 
    exp_id = exp_list[0].id
```

After retrieving the experiment id the next step is to create the metadata for the algorithm to run.

For this example the toy algorithm and its corresponding metadata is chosen but any other algorithm can
be used according to the general setup available here.

Importing the protobuf definitions of the metadata helps with typings and makes the development experience easier.
The TQ42 Python SDK however expects you to pass in the metadata as a dictionary and so using the `MessageToDict` function
is helpful to create the perfect matching dictionary while getting type hints.

Note: You can find all types corresponding to the algorithms within `tq42.algorithm`.

```python
from google.protobuf.json_format import MessageToDict
from tq42.algorithm import (
    ToyMetadataProto,
    ToyParametersProto,
    ToyInputsProto
)

toy_params = ToyMetadataProto(
    parameters=ToyParametersProto(n=1, r=1.5, msg='This is my first experiment run'),
    inputs=ToyInputsProto()
)
toy_params = MessageToDict(toy_params, preserving_proto_field_name=True)
```

After creating the available metadata and retrieving an experiment id the last step is to actually create the experiment run.

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun
from tq42.algorithm import AlgorithmProto
from tq42.compute import HardwareProto

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        # you can configure the algorithm to run here via the supplied enum
        # be sure to choose matching algorithm and parameters as this will be validated by our backend
        algorithm=AlgorithmProto.TOY,
        # pass in your experiment id here
        experiment_id=exp_id,
        # you can configure the hardware choice here via the supplied enum
        compute=HardwareProto.SMALL,
        # choose your dictionary here
        parameters=toy_params
    )
```

The experiment run can now be found via the UI and checked for its status.

Alternatively, you can also use either the SDK or CLI to check on the experiment run.
For more details om these two please take a look into the corresponding section of the documentation.

For more details on specific algorithms please take a look at the individual sections.
