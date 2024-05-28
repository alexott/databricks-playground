# Tool to bulk deactivating/reactivating Databricks users and service principals inside the workspace

This directory contains the `deactivate-activate-users-sps.py` script that allows to deactivate all non-admin users and service principals in the Databricks workspace, and store the list in the config file.  And then it's possible to reactivate them based on the stored data.

## Installation

You need to have [Databricks SDK for Python](https://pypi.org/project/databricks-sdk/) installed to run this tool.  Do

```sh
pip install databricks-sdk
```

to install SDK


## Running

You must configure environment variables to perform [authentication](https://pypi.org/project/databricks-sdk/#authentication) to a Databricks workspace where work will be done.

Use `-h` command-line option to get help on supported commands:

```
usage: deactivate-activate-users-sps.py [-h] [--file FILE] [--debug] [--verbose] {scan,deactivate,reactivate}

Deactivate or reactivate Databricks users and service principals

positional arguments:
  {scan,deactivate,reactivate}

options:
  -h, --help            show this help message and exit
  --file FILE           File to store deactivated users/SPs (default: deactivated_users.json)
  --debug               Enable debug output
  --verbose             Enable verbose output
```

There are three commands supported

* `scan` just prints a list of active users and service principals that aren't part of `admins` group.
* `deactivate` finds all active non-admin users and service principals and deactivate them.  Information about deactivated users/SPs is stored in the file that then will be used with `reactivate` command.
* `reactivate` reads the previously generated file and reactivates users and service principals.


Optionally, you can use `--file` command line option to change the file name where we store data about deactivated users/SPs (default file name is `deactivated_users.json`).



## TODOs


- \[ \] Better error handling.
