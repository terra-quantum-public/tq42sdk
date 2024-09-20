![](banner.png)

# Introduction to TQ42

The [TQ42 Python SDK](https://github.com/terra-quantum-public/tq42sdk) puts the power in your hands to accelerate
delivery of custom, high-impact solutions. After installing the SDK and authenticating, access algorithms such as:

- **TetraOpt** – a global optimization library based on tensor train (TT) decomposition.
- **ClearVu Analytics (CVA)** – build predictive models for data driven insights, automated ML and optimization.
- **Quantum Encoding (QuEnc)** – a gradient-based optimization algorithm tailored for hardware-efficient quantum
  circuits utilizing amplitude encoding.
- **TQnet** – train and apply custom, sequential hybrid quantum-classical neural networks with our comprehensive
  library.

With TQ42, there is no need to build or manage your own quantum circuits. Let our algorithms do the work. From the CLI,
your Python IDE, or a Jupyter notebook:

- Set up your environment to work in the correct organization, project, and experiment
- Connect a dataset, if needed, or use communication channels
- Specify your objective function, hyperparameters, and compute infrastructure
- Run and manage experiments
- Visualize results

Collaborate with your teams across organizations and projects, and visit
the [TQ42 web interface](https://terraquantum.io) for web-based tools to help you manage your account, projects, and
experiments.

# TQ42 Features

![](infographic.jpg)

# Getting Started

## System Requirements

Be sure your system can support TQ42, which requires the following:

- Any modern operating system, in particular, macOS 12.0 (Ventura) or above, Windows 10+, Linux will do
- Python 3.8 or above
- 256 MB RAM
- approx. 260 MB free disk space

The following Python packages are hard dependencies, and will automatically be installed alongside TQ42:

- [protobuf](https://googleapis.dev/python/protobuf/latest/)
- [grpcio-tools](https://pypi.org/project/grpcio-tools/)

## Quick Start

List of commands to execute to have a conda environment ready to work with the sdk.
After having installed [conda](https://docs.anaconda.com/free/anaconda/install/index.html):

```bash
conda create -n "my_env_name" python=3.9  # create the conda enviroment, it needs to be python 3.8 or higher
conda activate my_env_name                # activate your conda enviroment
pip install -U tq42                       # install the sdk using the newest available version
pip install jupyter                       # install jupyter if you work with notebook
pip install jupyter matplotlib            # install matplotlib for visualization purpose
tq42 auth login                           # authenticate the user 
tq42 -h                                   # for visualizing the help
```

## Installation

Prior to installing TQ42, create a virtual environment or conda environment.

- [virtual environment](https://docs.python.org/3/library/venv.html)
- [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

TQ42 is published on pypi, so on x86_64, i686, ppc64le, s390x, and aarch64 Linux systems, x86_64 or ARM (Apple Silicon)
on macOS, and 32 and 64-bit Windows installing is as simple as running the `pip install tq42` command:

```bash
pip install tq42
```

NOTE: We will refer to `pip` rather than `pip3`. Depending on how your system is configured you may have to use `pip3`
rather than `pip` if the alias is not set.

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

This API call will open a window in your browser where you must confirm the MFA code, then enter your TQ42 username and
password to authenticate.

The authentication validity will keep extending as long as you are using it within a 30 day period.

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

```python
toy_params = {
    'parameters': {
        'n': 1,
        'r': 1.5,
        'msg': 'This is my first experiment run'
    }
}
```

After creating the available metadata and retrieving an experiment id the last step is to actually create the experiment
run.

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

The experiment run can now be found via the UI and checked for its status.

Alternatively, you can also use either the SDK or CLI to check on the experiment run.
For more details om these two please take a look into the corresponding section of the documentation.

For more details on specific algorithms please take a look at the individual sections.

# TQ42 Help Center

TQ42 offers a dedicated Help Center, allowing you to access a wide range of support and learning materials, including:

- Video tutorials on SDK processes.
- Help articles across a range of platform workflows, including organisation and project configuration, inviting team
  members and running experiments.
- A scientific knowledge base – including articles on quantum computing, machine learning, optimization, simulation and
  our flagship algorithms.

Please visit our [Help Center Homepage](https://help.terraquantum.io/).

Customers can also contact our Customer Support team via the Help Centre using the help widget. Here, you can:

- Contact our team for technical support
- Report a bug on our platform
- Suggest an improvement on TQ42.

Our Help Center can also be accessed via CLI and Python specific commands. Please see the appropriate developer guides
further through our SDK documentation for more information. 
