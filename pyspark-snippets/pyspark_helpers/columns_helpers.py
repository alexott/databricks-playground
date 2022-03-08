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
