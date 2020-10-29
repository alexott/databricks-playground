name := "dbconnect-sbt"

organization := "net.alexott.demos.databricks"

version := "0.1"

scalaVersion := "2.12.12"
scalacOptions ++= Seq("-Xmax-classfile-name", "78")

//// default value
val jarsPathManual = ""

unmanagedBase := {
 import java.nio.file.{Files, Paths}
 import scala.sys.process._

 val jarsPathEnv = System.getenv("DBCONNECT_JARS")
 if (jarsPathEnv != null && Files.isDirectory(Paths.get(jarsPathEnv))) {
   // println("We have path from the environment variable! " + jarsPathEnv)
   new java.io.File(jarsPathEnv)
 } else {
   val paramPathEnv = System.getProperty("DbConnectJars")
   if (paramPathEnv != null && Files.isDirectory(Paths.get(paramPathEnv))) {
     // println("We have path from the system parameter! " + paramPathEnv)
     new java.io.File(paramPathEnv)
   } else {
     val dbConenctPath: String = try {
       Seq("databricks-connect", "get-jar-dir").!!.trim
     } catch {
       case e: Exception =>
         // println(s"Exception running databricks-connect: ${e.getMessage}")
         ""
     }
     if (!dbConenctPath.isEmpty && Files.isDirectory(Paths.get(dbConenctPath))) {
       // println("We have path from the databricks-connect! " + dbConenctPath)
       new java.io.File(dbConenctPath)
     } else if (Files.isDirectory(Paths.get(jarsPathManual))) {
       // println("We have path from the manual path! " + jarsPathManual)
       new java.io.File(jarsPathManual)
     } else {
       throw new RuntimeException("Can't find DB jars required for build! Set DBCONNECT_JARS environment variable, set -DDbConnectJars=path in .sbtopts, activate conda environment, or set the 'jarsPathManual' variable")
     }
   }
 }
}

// Example how to use OSS Spark dependencies, to use, comment out the 'unmanagedBase' piece
// val sparkVersion = "3.0.1"
// libraryDependencies += "org.apache.spark" %% "spark-core" % sparkVersion % Provided
// libraryDependencies += "org.apache.spark" %% "spark-sql" % sparkVersion % Provided
// libraryDependencies += "org.apache.spark" %% "spark-hive" % sparkVersion % Provided
