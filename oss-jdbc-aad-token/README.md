# Querying Databricks via JDBC with AAD token

This directory contains the example of querying data via Databricks SQL Endpoint or Databricks Cluster using JDBC protocol and Databricks OSS JDBC driver.   The JDBC driver supports OAuth authentication. Following examples demonstrate that:

* `OssJDBCAadTokenUser` - authentication to Databricks is performed using Azure Active Directory tokens issued for the current user.
* `OssJDBCAadTokenServicePrincipal` - authentication to Databricks is performed using Azure Active Directory tokens issued for Azure Service Principal.

## Adjusting parameters

Right now many parameters are hard-coded, so you need to change them before running.

### For `OssJDBCAadTokenServicePrincipal`

You need to update source code and adjust following parameters:

* `query` - what query should be executed
* `clientId` - client ID of application in Azure Active Directory
* `clientSecret` - secret for AAD application (ideally should be taken from KeyVault);
* `host` - the host portion of the Databricks workspace (obtained from SQL Warehouse configuraiton)
* `httpPath` - the HTTP Path of the SQL Warehouse (obtained from SQL Warehouse configuraiton)

### For `OssJDBCAadTokenUser`

* `query` - what query should be executed
* `host` - the host portion of the Databricks workspace (obtained from SQL Warehouse configuraiton)
* `httpPath` - the HTTP Path of the SQL Warehouse (obtained from SQL Warehouse configuraiton)
* `oauthClientId` - (optional) if you don't have Azure application with name `databricks-sql-jdbc`, then set it to the Application ID of the Azure application that will be used for authentication.

## Build & run

Just execute `mvn package` to build the code, and then you can execute resulting uber jar:

```sh
java -cp target/oss-jdbc-aad-token-0.0.2-jar-with-dependencies.jar \
  net.alexott.demos.OssJDBCAadTokenServicePrincipal
```

Or the code could be executed from an IDE.
