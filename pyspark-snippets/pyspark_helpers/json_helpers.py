import pyspark.sql.functions as F
from pyspark.sql import SparkSession


def schema_of_json(line: str) -> str:
  """
  Returns a Spark DDL string
  :param line: string with JSON data
  :return: Spark DDL string
  """
  df = SparkSession.getActiveSession().range(1).select(F.schema_of_json(F.lit(line)))
  return df.collect()[0][0]
