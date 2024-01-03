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
--compute="COMPUTE_NAME"
```


For more information on how to include this flag in your run command, see **Submitting and Monitoring a Run**. 

## Viewing Available Compute Resources and Configuration Details

For a list of the available compute resources, type `tq42 compute list`:
```bash
tq42 compute list
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


If you need more details on what each of the compute configurations includes, type `tq42 compute show-details`: 
```bash
tq42 compute show-details
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

Optionally, you may append the `--compute="COMPUTE_NAME"` flag for the specific compute type to view the details only for that configuration.
```bash
tq42 compute show-details --compute="COMPUTE_NAME"
```

For example:
```bash
tq42 compute show-details --compute="SMALL"
SMALL
CPUs = (#)
Memory = (#)
Storage = (enter text)
GPU = (N/A)
```