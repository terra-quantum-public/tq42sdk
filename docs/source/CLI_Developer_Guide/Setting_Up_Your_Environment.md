# Setting Up Your Environment

## Check Your Current Organization and Project Settings

Since users may belong to multiple organizations, or may be a member of several projects (each with their own budgets), before running an experiment it is important to check that you are working within the correct organization and project.

To check your current organization and project, type `tq42 proj show`:
```bash
tq42 proj show
```

The output is the following, where the current organization, project ID and associated project friendly name (if any) are shown:

`org="ORG_ID"`

`proj="Friendly name" (proj_id)`

For example:
```bash
tq42 proj show
org="5bac0b60-48d0-45cd-bf0a-39505b058106"
proj="Hitchhikers Routing Optimization" (7mvu9b58-51p7-42ae-eh0q-71305c413945)
```


## List All Organizations

To list all the organizations you have permission to view, type `tq42 org list`:
```bash
tq42 org list
```

The output is the following, where the system will return a list of orgs you have permission to view:

`org="ORG_ID"`

`org="ORG_ID"`

For example:
```bash
tq42 org list
org="5bac0b60-48d0-45cd-bf0a-39505b058106"
org="8b623343-1e0b-4a9e-a9fd-6dd6d0d1368c"
```


## List All Projects

To list all the projects you have permission to view within the organization that is currently set, type `tq42 proj list`:
```bash
tq42 proj list
```

The system will return a list of available projects (and their associated friendly names) belonging to the current organization, such as this:

`proj="Friendly name" (proj_id)`

`proj="Friendly name" (proj_id)`

For example:
```bash
tq42 proj list
proj="Hitchhikers Routing Optimization" (7mvu9b58-51p7-42ae-eh0q-71305c413945)
proj="Vessel Routing" (b2651e9f-9613-43ab-8b45-4dce84f5e92c)
```


To show the projects within a different organization than the one that is currently set, append the `--org="ORG_ID"` flag to the `tq42 proj list` command:
```bash
tq42 proj list --org="ORG_ID"
```


## List All Experiments

To list all the experiments you have permission to view within the project that is currently set, type `tq42 exp list`:
```bash
tq42 exp list
```

The system will return a list of available experiments (and their associated friendly names) belonging to the current project, such as this:

`exp="Friendly name" (exp_id)`

`exp="Friendly name" (exp_id)`

`exp="Friendly name" (exp_id)`

For example:
```bash
tq42 exp list
exp="Simple Route" (25dcabf9-72b3-4a10-8195-4f96c8dbf7f0)
exp="Complex Route v1" (19a4b843-d5c3-4e43-8579-64166e55f3ae)
exp="Complex Route v2" (23e9715e-6f0e-4819-b9f2-88db9ef0a599)
exp="Routing Option 1" (e9a8fc1d-3a9b-4867-9812-d98db90c8b5a)
```


To show the experiments within a different project than the one that is currently set, append the `--proj="PROJ_ID"` flag to the `tq42 exp list` command, where `"PROJ_ID"` contains the project ID you want to look up:
```bash
tq42 exp list --proj="PROJ_ID"
```


## List All Runs within an Experiment

To list all the runs within an experiment you have permission to view, type the `tq42 exp run list` command with the flag `--exp="EXP_ID"`, where `"EXP_ID"` contains the experiment ID you want to look up:
```bash
tq42 exp run list --exp="EXP_ID"
```

The system will return a list of available runs within the specified experiment, such as this:

`run="RUN_ID"`

`run="RUN_ID"`

`run="RUN_ID"`

For example:
```bash
tq42 exp run list --exp="25dcabf9-72b3-4a10-8195-4f96c8dbf7f0"
run="7e8a70b5-5c4d-48fd-95c0-034a2b2a8288"
run="d7fc2963-9dc5-4a6a-8d27-6d8db4178c84"
run="1d7ca856-65b4-4e16-a3d3-d0577268809a"
```

## Changing Your Workspace to a Different Organization or Project

To change the organization you are working within, type the `tq42 org set "ORG_ID"` command, where the `"ORG_ID"` quotes contain the organization ID:
```bash
tq42 org set "ORG_ID"
```

The system will change the active organization and confirm the org ID. The system will also return the default project ID for that organization so you know which project you are currently working within by default:

`org="ORG_ID"`

`proj="Friendly name" (proj_id)`

For example:
```bash
tq42 org set "8b623343-1e0b-4a9e-a9fd-6dd6d0d1368c"
org="8b623343-1e0b-4a9e-a9fd-6dd6d0d1368c"
proj="Hitchhikers Routing Optimization" (7mvu9b58-51p7-42ae-eh0q-71305c413945)
```

To change the project, type the `tq42 proj set "PROJ_ID"` command, where the `"PROJ_ID"` quotes contain the project ID:
```bash
tq42 proj set "PROJ_ID"
```

The system will change the active project and confirm the org ID as well as the project ID:

`org="ORG_ID"`

`proj="Friendly name" (proj_id)`

For example:
```bash
tq42 proj set "93fd91ef-43a1-4c3d-ba42-ebaa48cde3e0"
org="5bac0b60-48d0-45cd-bf0a-39505b058106"
proj="Windmill ML Energy Forecasting" (93fd91ef-43a1-4c3d-ba42-ebaa48cde3e0)

```


## Setting Friendly Names for Projects and Experiments

The ID strings for Projects and Experiments can be difficult to navigate due to their length and complexity. To make it easier to reference, you can set a friendly name for Projects and Experiments from the CLI or Python tools, or from the TQ42 user interface. Note: updating the friendly names for a Project or Experiment in one place will update it everywhere, and will be visible to all team members who have access to that Project or Experiment. It is not possible to set a friendly name for an organization.

To set a friendly name for a project so it is easier to reference than the `PROJ_ID` string, type `tq42 proj set-friendly-name` and provide a `"FRIENDLY_NAME"` as well as the `--proj="PROJ_ID"` flag:
```bash
tq42 proj set-friendly-name "FRIENDLY_NAME" --proj="PROJ_ID"
```


The system will change the friendly name for that project and automatically return the friendly name value so you can confirm it:

`proj="Friendly name" (proj_id)`

For example:
```bash
tq42 proj set-friendly-name "Fleet Routing" --proj="23e9715e-6f0e-4819-b9f2-88db9ef0a599"
proj="Fleet Routing" (23e9715e-6f0e-4819-b9f2-88db9ef0a599)
```

To set a friendly name for an experiment so it is easier to reference than the `EXP_ID` string, type `tq42 proj set-friendly-name` and provide a `"FRIENDLY_NAME"` as well as the `--exp="EXP_ID"` flag:
```bash
tq42 exp set-friendly-name "FRIENDLY_NAME" --exp="EXP_ID"
```


The system will change the friendly name for that experiment and automatically return the friendly name value so you can confirm it:

`exp="Friendly name" (exp_id)`

For example:
```bash
tq42 exp set-friendly-name "Routing Option 1" --exp="e9a8fc1d-3a9b-4867-9812-d98db90c8b5a"
exp="Routing Option 1" (e9a8fc1d-3a9b-4867-9812-d98db90c8b5a)
```
