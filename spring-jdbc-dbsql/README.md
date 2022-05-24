# Querying Databricks via JDBC using Spring JDBC

This directory contains the example of querying data via Databricks SQL Endpoint or Databricks Cluster using JDBC protocol.  Authentication to Databricks is performed using Databricks personal access token. 


## Adjusting parameters

You need to update source code and adjust following parameters:

* `query` - what query should be executed
* `host` - hostname of Databricks workspace obtained as per [documentation](https://docs.databricks.com/integrations/bi/jdbc-odbc-bi.html#jdbc-configuration-and-connection-parameters),
* `httpPath` - HTTP Path of Databricks cluster or SQL Endpoint
* `token` - personal access token

## Build & run

Just execute `mvn package` to build the code, and then you can execute resulting uber jar:

```sh
java -cp target/pring-jdbc-dbsql-0.0.1-jar-with-dependencies.jar \
  net.alexott.demos.spring_jdbc.SimpleQuery
```

Or the code could be executed from an IDE.
