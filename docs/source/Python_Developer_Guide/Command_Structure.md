# Command Structure

The TQ42 Python API uses individual resource oriented classes focused on individual parts of the system.

Everything is evolving around the TQ42Client which can be used as a context manager, like this:

```python
from tq42.client import TQ42Client
from tq42.organization import Organization

with TQ42Client() as client:
    org = Organization(client=client, id="ORG_ID")
```

Typically, these individual modules (e.g. `tq42.organization`) contain the following:

- resource oriented class
- `list_all` function returning a list of instances of the resource oriented class

**Example command for creating an ExperimentRun**

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun, HardwareProto

with TQ42Client() as client:
    ExperimentRun.create(
        client=client,
        experiment_id="EXP_ID",
        compute=HardwareProto.SMALL,
        algorithm='TOY',
        version='0.1.0',
        parameters={}
    )
```
