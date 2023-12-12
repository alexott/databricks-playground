# Querying Databricks SQL or cluster via Databricks SQL Python connector using AAD token

This directory contain demonstration of how to authenticate to Databricks using Azure Active Directory token when using [python-sql-connector](https://docs.databricks.com/dev-tools/python-sql-connector.html) library. There are three implementations:
1. `dbsql-with-aad-token-spn.py` using service principal and execute query against Databricks SQL Endpoint or Databricks Cluster.
2. `dbsql-with-aad-token-user.py` using user AAD interactive authentication.
2. `dbsql-with-aad-token-mi.py` using Azure Managed Identity associated with VM or AKS cluster.

## Installation

Install all necessary dependencies:

* `databricks-sql-connector`

by executing:

```sh
pip install -U -r requirements.txt
```

## Modify the script(s)

You need to modify scripts and change following variables:

* `host_name` - set to host name of the Databricks workspace (without `https://`)
* `http_path` - obtain HTTP Path parameter of Databricks SQL Endpoint or Databricks Cluster as per [documentation](https://docs.databricks.com/dev-tools/python-sql-connector.html#get-started).
* `query` - what query should be executed

### Set authentication parameters for dbsql-with-aad-token-spn.py

Authentication parameters of service principal could be set in the code directly (not the best way), or obtained from following environment variables:

* `ARM_TENANT_ID` - tenant ID in Azure Active Directory
* `ARM_CLIENT_ID` - client ID of application in Azure Active Directory
* `ARM_CLIENT_SECRET` - secret for AAD application

### Set authentication parameters for dbsql-with-aad-token-user.py

Authentication parameters of service principal could be set in the code directly (not the best way), or obtained from following environment variable:

* `ARM_CLIENT_ID` - client ID of application in Azure Active Directory that has user impersonation permission for Azure Databricks

### Set authentication parameters for dbsql-with-aad-token-mi.py

By default, the script will use default managed identity associated with the Azure VM or AKS. If you want to authenticate using a specific user-assigned managed identity, then set following environment variable.

* `ARM_CLIENT_ID` - client ID of user-assigned managed identity associated with VM or AKS.

## Execute script(s)

Just run:

```sh
python dbsql-with-aad-token-spn.py
```

or 

```sh
python dbsql-with-aad-token-user.py
```

or (only from VM with MI)

```sh
python dbsql-with-aad-token-mi.py
```

and it will print result of query execution.
