from pyspark.sql import SparkSession

from pyspark_helpers.data_skipping import reorder_columns


def test_data_skipping1(spark_session: SparkSession):
    original_df = spark_session.createDataFrame(
        [], schema="col1 string, col2 int, col3 string, col4 date")
    processed_df = reorder_columns(original_df)
    assert processed_df.columns == ["col2", "col4", "col1", "col3"]
    assert spark_session.conf.get(
        "spark.databricks.delta.properties.defaults.dataSkippingNumIndexedCols") == "2"


def test_data_skipping2(spark_session: SparkSession):
    original_df = spark_session.createDataFrame(
        [], schema="col1 string, col2 int, col3 string, col4 date")
    processed_df = reorder_columns(original_df, first_columns=["col3"])
    assert processed_df.columns == ["col3", "col2", "col4", "col1"]
    assert spark_session.conf.get(
        "spark.databricks.delta.properties.defaults.dataSkippingNumIndexedCols") == "3"


def test_data_skipping3(spark_session: SparkSession):
    original_df = spark_session.createDataFrame(
        [], schema="col1 string, col2 int, col3 string, col4 date")
    processed_df = reorder_columns(original_df, partition_columns=["col4"])
    assert processed_df.columns == ["col2", "col4", "col1", "col3"]
    assert spark_session.conf.get(
        "spark.databricks.delta.properties.defaults.dataSkippingNumIndexedCols") == "1"


def test_data_skipping_no_automatic(spark_session: SparkSession):
    original_df = spark_session.createDataFrame(
        [], schema="col1 string, col2 int, col3 string, col4 date")
    processed_df = reorder_columns(original_df, first_columns=["col3", "col1"],
                                   automatic_indexing=False)
    assert processed_df.columns == ["col3", "col1", "col2", "col4"]
    assert spark_session.conf.get(
        "spark.databricks.delta.properties.defaults.dataSkippingNumIndexedCols") == "2"

