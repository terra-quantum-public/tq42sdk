# Selecting Compute Resources

## Selecting Compute Resources for Your Experiment Run

TQ42 offers several configurations for compute resources to accommodate a variety of experiment run sizes.
To prepare your experiment run for submission, indicate a pre-configured compute resource.

## Viewing Available Compute Resources and Configuration Details

For a list of the available compute resources, use the `list_all` function provided by the `tq42.compute` module.

```python
from tq42.compute import list_all

compute_options = list_all()
print(compute_options)
```

The function will return a list of compute instances.

If you need more details on what each of the compute configurations includes, use `show_details` function on this instance: 
```python
from tq42.compute import list_all

compute = list_all()[0]
print(compute.show_details())
```

Optionally, you may use the `HardwareProto` to specify a specific compute configuration to initialize the instance.

```python
from tq42.compute import Compute, HardwareProto

compute = Compute(hardware=HardwareProto.SMALL)
details = compute.show_details()
print(details)
```