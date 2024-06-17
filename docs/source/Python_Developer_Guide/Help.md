# Get Help

## Command-specific Help
For assistance with any of the commands, precede any command with the `help` flag for contextual guidance.
Visit https://help.terraquantum.io/ to access our help centre - access help articles and video tutorials, report bugs, contact support and request improvements.

For example, type the command:

```python
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun

with TQ42Client() as client:
    help(ExperimentRun)
```

This returns the contextual guidance about the `ExperimentRun` class.

## General Help
For general assistance, type this:
```python
from tq42.client import TQ42Client
help(TQ42Client)
```
