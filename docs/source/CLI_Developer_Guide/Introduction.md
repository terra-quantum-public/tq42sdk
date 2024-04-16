# Introduction

The TQ42 Command Line Interface (TQ42 CLI) enables you to interact with TQ42 services using commands in your command-line shell. With minimal configuration, the TQ42 CLI enables you to start running commands that implement functionality equivalent to that provided by the browser-based TQ42 platform from the command prompt in your terminal program.

## Prerequisites

For information about how to get started with the TQ42 SDK and its underlying dependencies, see the SDK README file here:  
https://github.com/terra-quantum-io/tq42sdk

## Authentication

To access TQ42 services with the TQ42 CLI, you need a TQ42 account. When running TQ42 CLI commands, the TQ42 CLI needs to have access to your TQ42 account credentials.

There are 2 ways to Authenticate, 
1. By using your TQ42 account in https://terraquantum.io/. 
    - Authenticate by typing the CLI command:

    ```bash
    tq42 auth login
    ```
    
    - This command will open a window in your browser where you must enter your TQ42 username and password to authenticate.
    
    - If you have previously authenticated and your credentials are still valid, you will be automatically authenticated. However, if your credentials have expired, you will see a prompt to authenticate and can re-authenticate using the command above.
   

2. By defining TQ42_AUTH_CLIENT_ID and TQ42_AUTH_CLIENT_SECRET in the environment variables.
    - This authentication doesn't require user interaction. 
    - Add the following environment variables in the command line.
   
    ```bash
   export AUTH_CLIENT_ID=your_auth_client_id
   export AUTH_CLIENT_SECRET=your_auth_client_secret
    ```

      - Then do the same as above:

    ```bash
    tq42 auth login
    ```
   
   You will then see the result below if it is successful:
    ```bash
   Authentication is successful, access token is saved in: keyring.
   org:a_uuid_of_your_org
   proj:a_uuid_of_your_project
    ```
