# Get Help

## Command-specific Help
For assistance with any of the commands, append the `--help` flag to any command for contextual guidance. 

For example, type the command:
```bash
tq42 org list --help
```

This returns the contextual guidance about the `tq42 org list` command.

For example:
```bash
tq42 org list --help

To list all the organizations you have permission to view, type the 'tq42 org list' command:
tq42 org list

The output is the following, where the system will return a list of orgs you have permission to view: 
org="ORG_ID"
org="ORG_ID"

For example:

tq42 org list
org="5bac0b60-48d0-45cd-bf0a-39505b058106"
org="8b623343-1e0b-4a9e-a9fd-6dd6d0d1368c"
```

## General Help
For general assistance, type the `tq42 --help` command:
```bash
tq42 --help
```

For example:
```bash
tq42 --help

Visit https://help.terraquantum.io/ for more detail on the following commands:

Mandatory commands:

tq42 auth login

tq42 exp run create \
    --exp="EXP_ID" \
    --compute="COMPUTE_NAME" \
    --algorithm="ALGORITHM_NAME" \
    --parameters="PARAMETERS_JSON"

---

Optional Commands:

tq42 proj show

tq42 org list

tq42 proj list

tq42 exp list

tq42 exp run list --exp="EXP_ID"

tq42 org set "ORG_ID"

tq42 proj set "PROJ_ID"

tq42 proj set-friendly-name "FRIENDLY_NAME" --proj="PROJ_ID"

tq42 exp set-friendly-name "FRIENDLY_NAME" --exp="EXP_ID"

tq42 compute list

tq42 compute show-details

tq42 exp run check "RUN_ID"

tq42 exp run poll "RUN_ID"

tq42 exp run cancel "RUN_ID"

positional arguments:
  {auth,compute,proj,exp,org,env}
    auth                Class to manage authentication
    compute             Class to show details about compute resources
    proj                Class to manage projects
    exp                 Class to manage experiments
    org                 Class to manage organization
```
