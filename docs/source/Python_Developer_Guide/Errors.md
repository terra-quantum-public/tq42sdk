# Errors
This page contains common errors you may encounter when using TQ42. If you need further assistance, please visit [TQ42 Help](https://terra-quantum-tq42sdk-docs.readthedocs-hosted.com/en/latest/) or contact our support team at support@terraquantum.swiss.

## Authentication Expired
`User Not Logged In: Authentication Required`

You are not currently logged in. Please log in or authenticate to access this feature or command.

To log in with your username and password or stored token, use `TQ42Client().login()`.

If you need further assistance, please contact our support team at support@terraquantum.swiss.

## Unauthorized

`Unauthorized Access: Insufficient Permissions`

You do not have the necessary privileges to execute the requested command. Double check that the resource exists and contact your system administrator or request the appropriate access level.

Suggestions:

Verify that you have the required permissions to perform the command.

If you believe you should have access, contact your system administrator or request the necessary privileges.

Ensure that you are logged in with the correct user account.

## Network Error

`Network Connection Error`

Unable to establish a connection to the server.

Please check your internet connection and try again. If the problem persists, contact your network administrator or service provider for assistance.

## Invalid Command

`Invalid Command: ‘[variable]'`

The command you entered, `[variable]`, is not recognized. Please check the spelling and syntax of the command and try again.

For a list of available commands, type `help` or consult the documentation at [TQ42 Help](https://terra-quantum-tq42sdk-docs.readthedocs-hosted.com/en/latest/). For help with a specific command, type `help("command")`. For example, `help(Experiment)`.

## Resource Unavailable

`Resource Unavailable: 'example.txt'`

The resource you requested, `[example.txt]`, is currently unavailable. Please ensure that the resource exists and is accessible.

Suggestions:

1. Double-check the file name and path to ensure accuracy.

2. Verify that the resource is not currently in use or locked by another process.

3. If the resource is on a remote server, ensure that the network connection is stable and accessible.

4. If the resource was recently moved or deleted, consider restoring it from a backup or contacting your system administrator.

## No Default

Unable to Execute: `[command]`

We were unable to find the default org and/or proj ID required to run this command.
For a list of available commands, type `tq42 --help` or consult the documentation at tq42.com/help.

## Invalid Argument

Unable to Execute: `[command]`

We were unable to execute the given command as it violates certain constraints for the given resource:
[reason]

## Local Permission Issues

Unauthorized Access: Insufficient Local Permissions

You do not have the necessary privileges to write data locally.
Contact your system administrator or request the appropriate access level.