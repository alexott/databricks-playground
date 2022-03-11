## Checks compatibility of local Databricks connect environment with Databricks cluster

[`package_versions_check.py`](package_versions_check.py) - checks the versions of Python packages installed on the driver node & one of the executors.  I was using that to debug the "strange error" when using [dbconnect](https://docs.databricks.com/dev-tools/databricks-connect.html) when local environment had different versions of the packages than were used in the Databricks ML Runtime.
