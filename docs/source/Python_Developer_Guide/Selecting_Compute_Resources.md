# Selecting Compute Resources

## Selecting Compute Resources for Your Experiment Run

TQ42 offers several configurations for compute resources to accommodate a variety of experiment run sizes. To prepare your experiment run for submission, indicate a pre-configured compute resource. The options are:

- `compute="small"`
- `compute="medium"`
- `compute="large"`
- `compute="small_gpu"`
- `compute="medium_gpu"`
- `compute="large_gpu"`

One of these compute references must be included in your run command as a _flag_. For example, 
```bash
compute=COMPUTE_NAME
```


For more information on how to include this flag in your run command, see **Submitting and Monitoring a Run**. 

## Viewing Available Compute Resources and Configuration Details

For a list of the available compute resources, type `compute.list()`:

```python
from tq42.compute import list_all

compute_options = list_all()
```

The system will return the results:
```bash
SMALL
MEDIUM
LARGE
SMALL_GPU
MEDIUM_GPU
LARGE_GPU
```


If you need more details on what each of the compute configurations includes, type `tq42.compute.show_details()`: 
```python
    compute.show_details()
```

The system will return information about the configurations:
```bash
SMALL
CPUs = (#)
Memory = (#)
Storage = (enter text)
GPU = (N/A)

MEDIUM
CPUs = (#)
Memory = (#)
Storage = (enter text)
GPU = (N/A)

LARGE
CPUs = (#)
Memory = (#)
Storage = (enter text)
GPU = (N/A)

SMALL_GPU
CPUs = (#)
Memory = (#)
Storage = (enter text)
GPU = (details about type)

MEDIUM_GPU
CPUs = (#)
Memory = (#)
Storage = (enter text)
GPU = (details about type)

LARGE_GPU
CPUs = (#)
Memory = (#)
Storage = (enter text)
GPU = (details about type)
```

Optionally, you may append the `compute=COMPUTE_NAME` flag for the specific compute type to view the details only for that configuration.

```python
from tq42.compute import Compute

compute = Compute(hardware=HARDWARE_NAME)
details = compute.show_details()
```

For example:
```python
from tq42.compute import Compute

Compute(hardware="SMALL").show_details()
```

Will result in the following output:

```bash
name = SMALL
cpu = (#)
memory = (#)
storage = (enter text)
gpu = (N/A)
```