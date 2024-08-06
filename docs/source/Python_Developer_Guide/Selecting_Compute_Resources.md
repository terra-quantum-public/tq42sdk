# Selecting Compute Resources

## Selecting Compute Resources for Your Experiment Run

TQ42 offers several configurations for compute resources to accommodate a variety of experiment run sizes.
To prepare your experiment run for submission, indicate a pre-configured compute resource.

This can be chosen by using the `HardwareProto`

```python
from tq42.experiment_run import HardwareProto

# eg.
small_compute = HardwareProto.SMALL
```