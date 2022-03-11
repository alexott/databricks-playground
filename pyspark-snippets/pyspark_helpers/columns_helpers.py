from typing import List

import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Column


def columns_except(df: DataFrame, ex: List[str] = None) -> List[Column]:
    """
    Returns a new list of columns without specified columns
    :param df: dataframe
    :param ex: columns to exclude
    :return: new dataframe
    """
    if ex is None:
        ex = []

    return [F.col(cl) for cl in df.columns if cl not in ex]


def except_columns(df: DataFrame, ex: List[str] = None) -> DataFrame:
    """
    Creates a new dataframe without specified columns
    :param df: dataframe
    :param ex: columns to exclude
    :return: new dataframe
    """
    return df.select(*columns_except(df, ex))


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
