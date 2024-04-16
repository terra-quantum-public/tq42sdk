# Introduction

Interact with TQ42 services using Python commands. With minimal configuration, TQ42 enables you to start running commands that implement functionality equivalent to that provided by the browser-based TQ42 platform from a Jupyter notebook or your preferred Integrated Development Environment (IDE).

## Prerequisites

For information about how to get started with the TQ42 SDK and its underlying dependencies, see the SDK README file here:  
https://github.com/terra-quantum-io/tq42sdk.

## Authentication
There are 2 ways to Authenticate, 

1. By using your TQ42 User Account in https://terraquantum.io/:
    - This command will open a window in your browser where you must enter your TQ42 username and password to authenticate.

After installing TQ42, do the following in your jupyter notebook or python script:
   
   ```python
   from tq42.client import TQ42Client
   
   with TQ42Client() as client:
       client.login()
   ```


- The authentication validity will keep extending as long as you are using it within a 30 day period.

- You will then see the result below if it is successful:

```bash
   Authentication is successful, access token is saved in: [keyring or filepath(when system keyring isn't available)].
   org:a_uuid_of_your_org
   proj:a_uuid_of_your_project
```

2. By using Client Credential Flow: 
    - Define TQ42_AUTH_CLIENT_ID and TQ42_AUTH_CLIENT_SECRET in the environment variables.
    - This authentication doesn't require user interaction.
    - After defining the environment variables, you can authenticate in the same way:

Add the environment variables below to where tq42 was installed. Use the corresponding values that were provided.
```bash
   export TQ42_AUTH_CLIENT_ID=your_auth_client_id
   export TQ42_AUTH_CLIENT_SECRET=your_auth_client_secret
```

   ```python
   from tq42.client import TQ42Client
   
   with TQ42Client() as client:
     client.login()
   ```
  
   - Note: Currently, TQ42_AUTH_CLIENT_ID and TQ42_AUTH_CLIENT_SECRET needs to me manually requested. You can request one from: support@terraquantum.swiss.

   - The authentication validity can be set based on your requirements.

   You will then see the result below if it is successful:

```bash
   Authentication is successful, access token is saved in: [keyring or filepath(when system keyring isn't available)].
   org:a_uuid_of_your_org
   proj:a_uuid_of_your_project
```

## Working with Jupyter

Some of our examples include work we’ve performed in Jupyter. Visit https://jupyter.org/install to learn more and optionally install Jupyter.