package net.alexott.demos

import com.databricks.dbutils_v1.DBUtilsHolder.dbutils
import org.apache.spark.sql.SparkSession

object DbutilsDemo {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().getOrCreate()

    // test that Spark works correctly...
    val df = spark.range(100)
    df.show(5)

    // get AAD service principal secret from the secret scope
    val clientSecret = dbutils.secrets.get("test", "test")
    val aadTenantId = "..."
    val clientID = ""
    // setup authentication parameters
    spark.conf.set("fs.azure.account.auth.type", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.endpoint", s"https://login.microsoftonline.com/$aadTenantId/oauth2/token")
    spark.conf.set("fs.azure.account.oauth2.client.id", clientID)
    spark.conf.set("fs.azure.account.oauth2.client.secret", clientSecret)

    // list files on ADLS
    dbutils.fs.ls("abfss://test@test.dfs.core.windows.net/").foreach(println)
  }
}
