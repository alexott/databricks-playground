# Global & cluster init scripts for Databricks

This directory contains a collection of [global & cluster init scripts for Databricks](https://docs.databricks.com/clusters/init-scripts.html).


## Global init scripts

Many of these scripts could be used as cluster-level init scripts as well, but their main goal to configure all clusters in a workspace.  To use, just add their content via [Databricks Admin Console](https://docs.databricks.com/clusters/init-scripts.html#global-init-scripts), via [Terraform](https://registry.terraform.io/providers/databrickslabs/databricks/latest/docs/resources/global_init_script), or [REST API](https://docs.databricks.com/dev-tools/api/latest/global-init-scripts.html). 

* [`install-ssl-certificates.sh`](install-ssl-certificates.sh) - allows to install custom CA SSL certificates into all certificates chains - Linux, JVM and Python's certifi package.  This is required when organization uses an organization-specific  SSL certificate authority (CA), and want to avoid getting SSL certificate validation errors when accessing internal resources signed by that CA.  To use this script, upload to DBFS SSL CA certificate(s) in PEM format, and update list of paths on line 11 (`declare -a certs`).  Please note that you need to use `/dbfs/` instead of `dbfs:/`.



## Cluster-level init scripts
