# Example of using Databricks dbutils in JVM-based code compiled into .jar

This directory shows how to use Databricks dbutils from the code compiled into & deployed as `.jar` file.  It shows use of the `dbutils.secrets.get` and `dbutils.fs.ls` by listing files on ADLS using the service principal & SP secret is retrieved from secret scope (in my case, it was based on Azure KeyVault).

The main caveat is that when building a fat jar, the `dbutils` and Spark dependencies shouldn't be included into the resulting `.jar` file - it's done by marking these dependencies as `provided` in the `pom.xml`.

## Setup

1. Change secret scope & secret names in line 15 of `src/main/scala/net/alexott/demos/DbutilsDemo.scala`, update other variables to point to your ADLS account.
1. Compile using `mvn package`.
1. Copy `target/dbutils-in-jar-0.0.1-jar-with-dependencies.jar` to DBFS or cloud storage.
1. Create a Databricks job with "Jar task", specify `net.alexott.demos.DbutilsDemo` as main class, use "No isolation shared" Access Mode in cluster configuration as we're using direct access to ADLS.
1. Run job - it should produce a list of files/directories in your ADLS account.
