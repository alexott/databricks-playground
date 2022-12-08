from typing import List, Optional

import pyspark.sql.types as T
from pyspark.sql import DataFrame, SparkSession


def _is_indexable_column(typ) -> bool:
    """Returns true if the column is indexable for Delta Data skipping
    :param typ: Spark Type object
    :return: true if column is indexable
    """
    return (
            typ == T.IntegerType()
            or typ == T.TimestampType()
            or typ == T.DateType()
            or typ == T.DoubleType()
            or typ == T.FloatType()
            or typ == T.LongType()
    )


def reorder_columns(df: DataFrame, first_columns: Optional[List[str]] = None,
                    partition_columns: Optional[List[str]] = None,
                    automatic_indexing: bool = True):
    """Reorders columns of the dataframe to make them indexable for Delta Data Skipping. Besides the
    columns specified by ``first_columns`` parameter, all time & numeric columns are moved forward.
    On Databricks, it also sets the ``spark.databricks.delta.properties.defaults.dataSkippingNumIndexedCols``
    configuration, so when you're writing data first time, it will set ``delta.dataSkippingNumIndexedCols``
    property on the table.  For OSS, this property needs to be set explicitly.

    :param df: dataframe to process
    :param first_columns: list of additional columns that needs to be moved first
    :param partition_columns: list of columns that will be used for partitioning
    :param automatic_indexing: flag defining if we should automatically select columns for indexing (
    :return: modified dataframe
    """
    if first_columns is None:
        first_columns = []
    if partition_columns is None:
        partition_columns = []
    not_first_cols = [
        field for field in df.schema.fields if field.name not in first_columns
    ]
    if automatic_indexing:
        indexable_cols = [
            field.name for field in not_first_cols if _is_indexable_column(field.dataType)
        ]
        non_indexable_cols = [
            field.name for field in not_first_cols if not _is_indexable_column(field.dataType)
        ]
    else:
        indexable_cols = []
        non_indexable_cols = [field.name for field in not_first_cols]

    # Correct number of columns to index if column(s) is used for partitioning
    cols_len = len(first_columns + indexable_cols) - \
        len(set(partition_columns).intersection(set(first_columns + indexable_cols)))
    # TODO: think how this will be handled when doing multiple reorders inside the pipeline
    SparkSession.getActiveSession().conf.set(
        "spark.databricks.delta.properties.defaults.dataSkippingNumIndexedCols", str(cols_len),
    )
    return df.select(*first_columns, *indexable_cols, *non_indexable_cols)
