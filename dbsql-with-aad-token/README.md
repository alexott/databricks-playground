# Querying Databricks SQL or cluster using AAD token

This Python script demonstrates how to authenticate to Databricks using Azure Active Directory token of service principal and execute query against Databricks SQL Endpoint or Databricks Cluster using [python-sql-connector](https://docs.databricks.com/dev-tools/python-sql-connector.html) library.

## Installation

Install all necessary dependencies:
* azure-identity
* databricks-sql-connector

by executing:

```sh
pip install -U -r requirements.txt
```

## Modify the script

You need to modify script and change following variables:

* `host_name` - set to host name of the Databricks workspace (without `https://`)
* `http_path` - obtain HTTP Path parameter of Databricks SQL Endpoint or Databricks Cluster as per [documentation](https://docs.databricks.com/dev-tools/python-sql-connector.html#get-started).
* `query` - what query should be executed

## Set authentication parameters

Authentication parameters of service principal could be set in the code directly (not the best way), or obtained from following environment variables:

* `ARM_TENANT_ID` - tenant ID in Azure Active Directory
* `ARM_CLIENT_ID` - client ID of application in Azure Active Directory
* `ARM_CLIENT_SECRET` - secret for AAD application

## Execute script

Just run:

```sh
python dbsql-with-aad-token.py
```

and it will print result of query execution.
