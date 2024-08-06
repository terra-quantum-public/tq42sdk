# Selecting Compute Resources

## Selecting Compute Resources for Your Experiment Run

TQ42 offers several configurations for compute resources to accommodate a variety of experiment run sizes. To prepare your experiment run for submission, indicate a pre-configured compute resource. The options are:

- `compute="small"`
- `compute="large"`
- `compute="small_gpu"`
- `compute="large_gpu"`

One of these compute references must be included in your run command as a _flag_. For example, 
```bash
--compute="COMPUTE_NAME"
```