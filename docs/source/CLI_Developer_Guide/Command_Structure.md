# Command Structure

The TQ42 CLI uses a multipart structure on the command line that must be specified in this order:

1. The base call to the `tq42` program.

2. The top-level _group_, which typically corresponds to a TQ42 service supported by the TQ42 CLI.

3. The _subgroup_ that corresponds to a _group_.

4. The _command_ that specifies which operation to perform.

5. General TQ42 CLI options or parameters required by the operation. You can specify these in any order as long as they follow the first three parts. If an exclusive parameter is specified multiple times, only the last value applies.

```bash
tq42 <group> <subgroup> <command> [options and parameters]
```

You can use commands (and groups / subgroups) alone or with one or more flags. A _flag_ is a term for any element other than the command or group name itself. A command or flag might also take an _argument_, for example, organization or project ID.

**Example command**
```bash
tq42 auth login
```

**Example command with a flag**
```bash
tq42 exp run list --exp="EXP_ID"
```

**Example command with multiple elements**
```bash
tq42 exp run create \
    --exp="EXP_ID" \
    --compute="COMPUTE_NAME" \
    --algorithm="ALGORITHM_NAME" \
    --parameters="PARAMETERS_JSON"
```

The preceding command consists of the following elements:

- `exp` is a `tq42` group.

- `run` is an `exp` subgroup.

- `create` is a `run` command.

- `--exp` is a flag set to an experiment to which the run should be assigned.

- `--compute` is a flag set to the pre-configured compute infrastructure you selected.

- `--algorithm` is a flag set to the algorithm name that should solve the problem.

- `--parameters` is a flag set to a JSON object containing constraints, hyper parameters, and possibly a URL for vectorized data or an objective function.