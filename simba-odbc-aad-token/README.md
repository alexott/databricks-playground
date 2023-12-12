# Querying Databricks SQL or cluster via Databricks ODBC driver using AAD token

This directory contain demonstration of how to authenticate to Databricks using Azure Active Directory token when using [Databricks ODBC driver](https://www.databricks.com/spark/odbc-drivers-download) via `pyodbc` library. There are two implementations:
1. `odbc-aad-service-principal.py` using service principal and execute query against Databricks SQL Endpoint or Databricks Cluster.
2. `odbc-aad-user.py` using user AAD interactive authentication.

## Installation

Install all necessary dependencies:

* `pyodbc`

by executing:

```sh
pip install -U -r requirements.txt
```

You also need to install ODBC driver as outlined in the [documentation](https://learn.microsoft.com/en-us/azure/databricks/integrations/jdbc-odbc-bi).

## Modify the script(s)

You need to modify scripts and change following variables:

* `host` - set to host name of the Databricks workspace (without `https://`)
* `http_path` - obtain HTTP Path parameter of Databricks SQL Endpoint or Databricks Cluster as per [documentation](https://docs.databricks.com/dev-tools/python-sql-connector.html#get-started).
* `driver` - location of ODBC driver library (i.e., `/Library/simba/spark/lib/libsparkodbc_sb64-universal.dylib` on Mac OS).
* `query` - what query should be executed

### Set authentication parameters for odbc-aad-service-principal.py

Authentication parameters of service principal could be set in the code directly (not the best way), or obtained from following environment variables:

* `ARM_CLIENT_ID` - client ID of application in Azure Active Directory
* `ARM_CLIENT_SECRET` - secret for AAD application

## Execute script(s)

Just run:

```sh
python odbc-aad-service-principal.py
```

or 

```sh
python odbc-aad-user.py
```

and it will print result of query execution.
