# An example of using Azure Managed Identity with Databricks Python SDK

This directory contains an example of using Azure Managed Identity with Databricks Python SDK. 
This is done by implementing a custom credential strategy that wraps the `azure-identity` package.

The code is in the `azure-mi-in-py-sdk.py` file - it instantiates a Databricks workspace client with 
the custom credential strategy and lists clusters in the workspace.  To run it you need to install
`databricks-sdk` and `azure-identity` packages (this could be done using the Poetry tool).

Managed identity (system or user-assigned) needs to be added into Databricks workspace.  The URL
of the Databricks workspace is specified via `DATABRICKS_HOST` environment variable or directly in 
the code (line 32).  It will be using default managed identity to generate token, but you can 
specify a different managed identity by setting `AZURE_CLIENT_ID` environment variable.
