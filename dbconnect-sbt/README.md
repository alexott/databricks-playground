This is an example of how SBT could be used to build project that uses jars from the [databricks-connect](https://docs.databricks.com/dev-tools/databricks-connect.html). Sometimes this is required because Databricks runtime (DBR) sometimes has more functionality than open source spark.  But in the most case it's enough to build a project using OSS Spark dependencies, and declare them as provided (shown as example in the `build.sbt`, as commented out code).

## Setup

To build the project following setup steps are necessary:

* Install Databricks Connect & Databricks CLI (better into a separate virtual Python/Conda environment - in this example, with name `test`.  For DBR 6.x we must to use Python 3.7!):

```sh
conda create --name test python=3.8
conda activate test
pip install -U databricks-connect==7.3 databricks-cli
export DBCONNECT_JARS=$(databricks-connect get-jar-dir)
export SPARK_HOME=$(dirname $DBCONNECT_JARS)
```

* Configure Databricks Connect as described in [documentation](https://docs.databricks.com/dev-tools/databricks-connect.html) - it's required if you want to run the artifact from your machine
* (optional) Configure Databricks CLI as described in [documentation](https://docs.databricks.com/dev-tools/cli/index.html)

## Build

To be able to compile & package this project you need to do following:

* (optional) Setting the location of the DB jars.  It could be configured by multiple ways, in order of execution:
  1. SBT will try to use the path from the environment variable `DBCONNECT_JARS` set above. 
  1. try to get path from the `DbConnectJars` system property - that's useful when you're running the project from the IDE.  It could be set in the `.sbtopts` file, for example, as `-DDbConnectJars=....` (execute in the root directory of the project following shell command: `echo "-DDbConnectJars=$(databricks-connect get-jar-dir)" |tee -a .sbtopts` to add this definition to the `.sbtopts` file)
  1. try to execute `databricks-connect get-jar-dir` if the `databricks-connect` is in the `PATH`
  1. take path from the `jarsPathManual` that is defined in the `build.sbt` - open it in the editor, and set this variable to the path to jars obtained via `databricks-connect get-jar-dir`
* Execute `sbt clean package` to build the project

## Executing from command-line

To run the built project from the command line we need to build the project with `sbt package` & execute following command:

```sh
$SPARK_HOME/bin/spark-submit --class net.alexott.demos.databricks.SimpleSQL target/scala-2.12/dbconnect-sbt_2.12-0.1.jar
```

In some cases you need to set environment variable `DEBUG_IGNORE_VERSION_MISMATCH` to value `1` because `spark-submit` checks if the databricks-connect checks for its version & fails if it doesn't match to the cluster's version.  And it could be a problem as databricks-connect isn't published for every DBR version.  You just need to make sure that you're using databricks-connect 6.x with DBR 6.x, and similarly for 7.x versions.

## Executing from Intellij Idea

The Ultimate version of Intellij Idea has [built-in support for submitting Spark jobs via spark-submit](https://www.jetbrains.com/help/idea/big-data-tools-spark-submit.html), so refer to documentation on how to configure it.

For Community Edition of Idea, we'll need to force the explicit submission of the Spark job by using the `SparkSubmit` class.  To configure this, go to the "Run" > "Edit Configurations..." and change settings as following:

* Main class: `org.apache.spark.deploy.SparkSubmit`
* VM options: `-cp $Classpath$:$SPARK_HOME`
* Program arguments: `--class net.alexott.demos.databricks.SimpleSQL target/scala-2.12/dbconnect-sbt_2.12-0.1.jar` - the `.jar` file should be built before execution, so it makes sense to hook `sbt package` into the "Before launch" configuration
* Environment variables: `SPARK_HOME=...` (put the value of `SPARK_HOME` defined above), and maybe `DEBUG_IGNORE_VERSION_MISMATCH=1` to allow to run on "incompatible" clusters.

After that you can execute Spark job directly from Idea.
