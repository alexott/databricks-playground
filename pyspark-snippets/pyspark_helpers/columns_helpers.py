from typing import List, Union, Optional

import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Column


def columns_except(df: DataFrame, ex: Optional[List[str]] = None, as_column: bool = False) -> List[Union[str, Column]]:
    """
    Returns a new list of columns without specified columns
    :param df: dataframe
    :param ex: columns to exclude
    :param as_column: if we should return list of columns instead of list of strings
    :return: new list of columns
    """
    if ex is None:
        ex = []

    return [F.col(cl) if as_column else cl
            for cl in df.columns if cl not in ex]


def dataframe_except_columns(df: DataFrame, ex: Optional[List[str]] = None) -> DataFrame:
    """
    Creates a new dataframe without specified columns
    :param df: dataframe
    :param ex: columns to exclude
    :return: new dataframe
    """
    return df.select(*columns_except(df, ex, as_column=True))


def add_missing_columns(df1: DataFrame, df2: DataFrame) -> DataFrame:
    """
    Adds to first dataframe columns from the second dataframe that don't exist in first one.
    Columns get null values casted to respective data types
    :param df1: first dataframe
    :param df2: second dataframe
    :return: new dataframe with added columns
    """
    additional_cols = [F.lit(None).cast(field.dataType).alias(field.name)
                       for field in df2.schema.fields if field.name not in df1.columns]
    return df1.select("*", *additional_cols)
