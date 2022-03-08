from typing import List

import pyspark.sql.types as T
from pyspark.sql import DataFrame, SparkSession


def _is_indexable_column(typ) -> bool:
    """Returns true if the column is indexable
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


def reorder_columns(df: DataFrame, first_columns: List[str] = None):
    """Reorders columns of the dataframe to make them indexable for Delta Data Skipping. Besides the
    columns specified by `first_columns` parameter, all time & numeric columns are moved forward

    :param df: dataframe to process
    :param first_columns: list of additional columns that needs to be moved first
    :return: modified dataframe
    """
    if first_columns is None:
        first_columns = []
    not_first_cols = [
        field for field in df.schema.fields if field.name not in first_columns
    ]
    indexable_cols = [
        field.name for field in not_first_cols if _is_indexable_column(field.dataType)
    ]
    non_indexable_cols = [
        field.name for field in not_first_cols if not _is_indexable_column(field.dataType)
    ]

    # TODO: think how this will be handled when doing multiple reorders inside the pipeline
    SparkSession.getActiveSession().conf.set(
        "spark.databricks.delta.properties.defaults.dataSkippingNumIndexedCols",
        str(len(first_columns + indexable_cols)),
    )
    return df.select(*first_columns, *indexable_cols, *non_indexable_cols)
