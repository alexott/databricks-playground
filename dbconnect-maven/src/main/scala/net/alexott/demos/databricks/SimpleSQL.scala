package net.alexott.demos.databricks

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object SimpleSQL {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("Simple SQL Test").getOrCreate()

    val df = spark.range(100000).withColumn("randc", rand())
    df.createOrReplaceTempView("my_sql_test")
    df.printSchema()
    spark.sql("select * from my_sql_test where randc > 0.9 limit 10").show(false)
  }

}
