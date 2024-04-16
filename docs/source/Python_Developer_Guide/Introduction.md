# Introduction

Interact with TQ42 services using Python commands. With minimal configuration, TQ42 enables you to start running commands that implement functionality equivalent to that provided by the browser-based TQ42 platform from a Jupyter notebook or your preferred Integrated Development Environment (IDE).

## Prerequisites

For information about how to get started with the TQ42 SDK and its underlying dependencies, see the SDK README file here:  
https://github.com/terra-quantum-io/tq42sdk.

## Authentication

To access TQ42 services with Python commands, you need a TQ42 account. When running TQ42 Python commands, your environment needs to have access to your TQ42 account credentials.

There are 2 ways to Authenticate, 
1. By using your TQ42 account in https://terraquantum.io/. 
    - This command will open a window in your browser where you must enter your TQ42 username and password to authenticate.

   
Procedure:

After installing TQ42, authenticate by typing `client.login()`.
   
   ```python
   from tq42.client import TQ42Client
   
   with TQ42Client() as client:
       client.login()
   ```

- If you have previously authenticated and your credentials are still valid, you will be automatically authenticated. However, if your credentials have expired, you will see a prompt to authenticate and can do so using the command above.
- The authentication validity will keep extending as long as you are using it within a 30 day period.

2. By defining AUTH_CLIENT_ID and AUTH_CLIENT_SECRET in the environment variables.
    - This authentication doesn't require user interaction.

Procedure:
   ```python
   from tq42.client import TQ42Client
   import os
   
   os.environ['TQ42_AUTH_CLIENT_ID'] = 'your_auth_client_id'
   os.environ['TQ42_AUTH_CLIENT_SECRET'] = 'your_auth_client_secret'
   
   with TQ42Client() as client:
       client.login()
   ```

   - Note: Currently, TQ42_AUTH_CLIENT_ID and TQ42_AUTH_CLIENT_SECRET needs to me manually requested. You can request one from: support@terraquantum.swiss.

   - The authentication validity can be set based on your requirements.



## Working with Jupyter

Some of our examples include work we’ve performed in Jupyter. Visit https://jupyter.org/install to learn more and optionally install Jupyter.