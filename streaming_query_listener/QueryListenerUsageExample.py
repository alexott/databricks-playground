# Databricks notebook source
# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

from query_listener import UcVolumeWriteListener

# COMMAND ----------

listener = UcVolumeWriteListener("/Volumes/main/tmp/tmp/stream1", "stream1")
spark.streams.addListener(listener)
read_df = spark.readStream.format("rate").load()
query1 = (
  read_df
    .writeStream
    .format("memory")
    .queryName("stream1")
    .trigger(processingTime="10 seconds")
    .start()
)

# COMMAND ----------

query1.stop()