This is an example of how Maven could be used to build Spark project that later will be executed via [databricks-connect](https://docs.databricks.com/dev-tools/databricks-connect.html).

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

This project is configured to be compiled with OSS Spark 3.0.1 that is compatible with DBR 7.x.  If you want to adapt it to another Databricks Runtime (DBR) version, then adjust properties `scala.version`, `spark.version`, and `spark.scala.version` to match Spark & Scala versions used in given DBR.

After that just execute `mvn clean package` to build the project.

## Executing from command-line

To run the built project from the command line we need to build the project with `mvn package` & execute following command:

```sh
$SPARK_HOME/bin/spark-submit --class net.alexott.demos.databricks.SimpleSQL target/dbconnect-maven-demo-0.0.1-jar-with-dependencies.jar
```

In some cases you need to set environment variable `DEBUG_IGNORE_VERSION_MISMATCH` to value `1` because `spark-submit` checks if the databricks-connect checks for its version & fails if it doesn't match to the cluster's version.  And it could be a problem as databricks-connect isn't published for every DBR version.  You just need to make sure that you're using databricks-connect 6.x with DBR 6.x, and similarly for 7.x versions.

## Executing from Intellij Idea

The Ultimate version of Intellij Idea has [built-in support for submitting Spark jobs via spark-submit](https://www.jetbrains.com/help/idea/big-data-tools-spark-submit.html), so refer to documentation on how to configure it.

For Community Edition of Idea, we'll need to force the explicit submission of the Spark job by using the `SparkSubmit` class.  To configure this, go to the "Run" > "Edit Configurations..." and change settings as following:

* Main class: `org.apache.spark.deploy.SparkSubmit`
* VM options: `-cp $Classpath$:$SPARK_HOME`
* Program arguments: `--class net.alexott.demos.databricks.SimpleSQL target/dbconnect-maven-demo-0.0.1-jar-with-dependencies.jar`. The `.jar` file should be built before execution, so it makes sense to hook `mvn package` into the "Before launch" configuration - select "Run Maven Goal" and put `package` there
* Environment variables: `SPARK_HOME=...` (put the value of `SPARK_HOME` defined above), and maybe `DEBUG_IGNORE_VERSION_MISMATCH=1` to allow to run on "incompatible" clusters.

After that you can execute Spark job directly from Idea.
