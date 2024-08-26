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

## Quick Start
List of commands to execute to have a conda environment ready to work with the SDK.
After having installed [conda](https://docs.anaconda.com/free/anaconda/install/index.html):
```bash
conda create -n "my_env_name" python=3.9  # create the conda environment, it needs to be Python 3.8 or higher
conda activate my_env_name                # activate your conda environment
pip install -U tq42                       # install the SDK using the newest available version
pip install jupyter                       # install Jupyter if you work with notebook
pip install jupyter matplotlib            # install matplotlib for visualization purpose
tq42 auth login                           # authenticate the user 
tq42 -h                                   # for visualizing the help

git clone git@github.com:terra-quantum-public/tq42sdk.git # cloning the repo in case you want to use the example's notebook 
```


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

This API call will open a window in your browser where you must confirm the MFA code, then enter your TQ42 username and password to authenticate.

The authentication validity will keep extending as long as you are using it within a 30-day period.

## Create an exemplary experiment run

After a successful login the next step is to create an experiment run.
An experiment run is nested inside an experiment, which is nested under a project (like a folder structure: Organization > Projects > Experiments > Experiment Runs). You can create experiments and projects via the [TQ42 web interface](https://terraquantum.io).

To supply the experiment run, the id of the created experiment is necessary.
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

```python
toy_params = {
    'parameters': {
        'n': 1,
        'r': 1.5,
        'msg': 'This is my first experiment run'
    }
}
```

After creating the available metadata and retrieving an experiment id the last step is to actually create the experiment run.

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun, HardwareProto

with TQ42Client() as client:
    run = ExperimentRun.create(
        client=client,
        # you can configure the algorithm to run here
        # be sure to choose matching algorithm, version and parameters as this will be validated by our backend
        algorithm='TOY',
        version='0.1.0',
        # pass in your experiment id here
        experiment_id=exp_id,
        # you can configure the hardware choice here via the supplied enum
        compute=HardwareProto.SMALL,
        # choose your dictionary here
        parameters=toy_params
    )
```

The experiment run can now be found via the [TQ42 web interface](https://terraquantum.io) and checked for its status.

Alternatively, you can also use either the SDK or CLI to check on the experiment run.
For more details on these two options, please take a look into the corresponding section of the documentation about monitoring an experiment run.

For more details on specific algorithms, please take a look at the individual sections.
