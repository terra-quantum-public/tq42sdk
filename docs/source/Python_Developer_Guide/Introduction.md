# Introduction

Interact with TQ42 services using Python commands. With minimal configuration, TQ42 enables you to start running commands that implement functionality equivalent to that provided by the browser-based TQ42 platform from a Jupyter notebook or your preferred Integrated Development Environment (IDE).

## Prerequisites

For information about how to get started with the TQ42 SDK and its underlying dependencies, see the SDK README file here:  
https://github.com/terra-quantum-io/tq42sdk.

## Authentication

To access TQ42 services with Python commands, you need a TQ42 account. When running TQ42 Python commands, your environment needs to have access to your TQ42 account credentials.

After installing TQ42, authenticate by typing `client.login()`.

```python
from tq42.client import TQ42Client

with TQ42Client() as client:
    client.login()
```

This command will open a window in your browser where you must enter your TQ42 username and password to authenticate.

If you have previously authenticated and your credentials are still valid, you will be automatically authenticated. However, if your credentials have expired, you will see a prompt to authenticate and can re-authenticate using the command above.

## Working with Jupyter

Some of our examples include work we’ve performed in Jupyter. Visit https://jupyter.org/install to learn more and optionally install Jupyter.