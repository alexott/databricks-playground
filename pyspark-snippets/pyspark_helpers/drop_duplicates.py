from typing import List, Dict, Any

from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession


def drop_duplicates_with_merge(
        df: DataFrame,
        primary_key_columns: List[str],
        path: str = "",
        table_name: str = "",
        partitionby: List[str] = None,
        opts: Dict[str, Any] = None,
):
    """Performs removal of duplicates using the Delta MERGE operation.  If table doesn't exist,
    it's created by writing the dataframe into a specified location.  This function is primarily
    designed for use in ``foreachBatch``.

    :param df: new dataframe
    :param primary_key_columns: required list of the column names that are used for detection of duplicates
    :param path: optional path to table (required if table_name isn't specified)
    :param table_name: optional name of the table (required if path isn't specified)
    :param partitionby: optional list of columns to partition by
    :param opts: optional dictionary with options for creation of Delta table
    :return: nothing
    """
    # print(f"Performing merge for {path=} or {table_name=}")
    if opts is None:
        opts = {}
    if partitionby is None:
        partitionby = []
    df = df.dropDuplicates(primary_key_columns)
    if path == "" and table_name == "":
        raise Exception(
            "At least one parameter, 'path' or 'table_name' must be specified"
        )
    if not df._jdf.isEmpty():
        try:
            spark = SparkSession.getActiveSession()
            if table_name != "":
                tbl = DeltaTable.forName(spark, table_name)
            else:
                tbl = DeltaTable.forPath(spark, path)
            dname = "dests"
            uname = "updates"
            merge_cond = " and ".join(
                [f"{dname}.{col} <=> {uname}.{col}" for col in primary_key_columns]
            )
            tbl.alias(dname).merge(
                df.alias(uname), merge_cond
            ).whenNotMatchedInsertAll().execute()
        # except AnalysisException as ex: # this happens when table doesn't exist
        except:  # this happens when table doesn't exist
            # print(f"Delta table ({path=}, {table_name=}) doesn't exist, writing all data as new table...")
            if table_name != "":
                if path != "":
                    opts["path"] = path
                df.write.format("delta").partitionBy(partitionby).options(
                    **opts
                ).saveAsTable(table_name)
            else:
                df.write.format("delta").partitionBy(partitionby).options(**opts).save(
                    path
                )


def drop_duplicates_builtin(
        df: DataFrame,
        primary_key_columns: List[str],
        watermark_column: str = None,
        watermark_time: str = None,
):
    """Performs deletion of duplicates on the given dataframe using the `.dropDuplicates` function.
    :param df: dataframe to process
    :param primary_key_columns: required list of the column names that are used for detection of duplicates
    :param watermark_column: optional column name that will be used for watermark in the streaming mode.
    :param watermark_time:
    :return: modified dataframe
    """
    if "watermark_column" and "watermark_time":
        if not df.isStreaming:
            raise Exception("Can't set watermark on the non-streaming dataframe")
        df = df.withWatermark(watermark_column, watermark_time)
    return df.dropDuplicates(primary_key_columns)
