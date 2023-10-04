# Querying Databricks SQL or cluster using AAD token

This directory contain demonstration of how to authenticate to Databricks using Azure Active Directory token when using [python-sql-connector](https://docs.databricks.com/dev-tools/python-sql-connector.html) library. There are two implementations:
1. `dbsql-with-aad-token-spn.py` using service principal and execute query against Databricks SQL Endpoint or Databricks Cluster.
2. `dbsql-with-aad-token-user.py`

## Installation

Install all necessary dependencies:
* databricks-sql-connector

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


## Execute script(s)

Just run:

```sh
python dbsql-with-aad-token-spn.py
```

or 

```sh
python dbsql-with-aad-token-user.py
```

and it will print result of query execution.
