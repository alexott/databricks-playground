# pyspark-snippets

This directory contains a number of functions that simplify development of PySpark code for Databricks.


## Building

```sh
python setup.py clean --all && python setup.py bdist_wheel --universal
```

## Testing

You need to install packages that are necessary for execution of tests:

```
pip install -U -r unit-requirements.txt
```

### Unit testing

Just execute:

```
pytest tests/unit
```

