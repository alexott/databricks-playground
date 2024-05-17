# Tool to bulk pausing/unpausing of Databricks Workflows

This directory contains the `pause_unpause_jobs.py` script that allows to pause all Workflows in the Databricks workspace, and store the list in the config file.  And then it's possible to unpause them based on the stored data.

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
usage: pause_unpause_jobs.py [-h] [--file FILE] {scan,pause,unpause}

Pause or unpause Databricks jobs with schedules or triggers

positional arguments:
  {scan,pause,unpause}

options:
  -h, --help            show this help message and exit
  --file FILE           File to store paused jobs (default: paused_jobs.json)
```

There are three commands supported

* `scan` just prints a list jobs that have a trigger or a schedule in the `UNPAUSED` status.
* `pause` finds all workflows with `UNPAUSED` status and pause them.  Information about paused tasks is stored in the file that then will be used with `unpause` command.
* `unpause` reads the previously generated file and unpause paused Workflows.


Optionally, you can use `--file` command line option to change the file name where we store data about paused tasks (default file name is `paused_jobs.json`).



## TODOs


- \[ \] Better error handling - for example, if a specific Databricks workflow is deleted.
