from typing import List

import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def except_columns(df: DataFrame, ex: List[str] = None) -> DataFrame:
    """
    Creates a new dataframe without specified columns
    :param df: dataframe
    :param ex: columns to exclude
    :return: new dataframe
    """
    if ex is None or len(ex) == 0:
        return df

    return df.select(*[F.col(cl) for cl in df.columns if cl not in ex])
