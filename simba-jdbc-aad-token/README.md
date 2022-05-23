# Querying Databricks via JDBC with AAD token

This directory contains the example of querying data via Databricks SQL Endpoint or Databricks Cluster using JDBC protocol.  Authentication to Databricks is performed using Azure Active Directory tokens issued for Azure Service Principal.  Package contains two similar examples that differ only by which library is used to generate AAD token:

* `SimbaJDBCAadTokenMsal` - uses [Microsoft Authentication Library (MSAL)](https://docs.microsoft.com/en-us/azure/active-directory/develop/msal-overview) - it's a recommended way of generating AAD tokens. 
* `SimbaJDBCAadTokenAdal` - uses old [Microsoft Azure Active Directory Authentication Library (ADAL)](https://github.com/AzureAD/azure-activedirectory-library-for-java) that isn't recommended to use.  Source code is just kept for reference.


## Installation of dependencies

## Adjusting parameters

You need to update source code and adjust following parameters:

* `query` - what query should be executed
* `tenantId` - tenant ID in Azure Active Directory
* `clientId` - client ID of application in Azure Active Directory
* `clientSecret` - secret for AAD application (ideally should be take from KeyVault);
* `jdbcString` - **JDBC string** obtained as per [documentation](https://docs.databricks.com/integrations/bi/jdbc-odbc-bi.html#jdbc-driver), and modified as following - replace `;AuthMech=3;UID=token;PWD=<personal-access-token>` with `;AuthMech=11;Auth_Flow=0;Auth_AccessToken=` (AAD token will be append to it), for example:

```
jdbc:databricks://<host>:443/default;transportMode=http;ssl=1;httpPath=<http-path>;AuthMech=3;UID=token;PWD=<personal-access-token>
```

should become:

```
jdbc:databricks://<host>:443/default;transportMode=http;ssl=1;httpPath=<http-path>;AuthMech=11;Auth_Flow=0;Auth_AccessToken=
```

## Build & run

Just execute `mvn package` to build the code, and then you can execute resulting uber jar:

```sh
java -cp target/simba-jdbc-aad-token-0.0.1-jar-with-dependencies.jar \
  net.alexott.demos.SimbaJDBCAadTokenMsal
```

Or the code could be executed from an IDE.
