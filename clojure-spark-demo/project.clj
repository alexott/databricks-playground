(defproject clojure-spark-demo "0.1.0-SNAPSHOT"
  :description "Example of Clojure project for Databricks"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.10.3"]
                 [zero.one/geni "0.0.40"
                  :exclusions [commons-codec reply nrepl org.nrepl/incomplete]];; 
                 [org.apache.spark/spark-sql_2.12 "3.2.1" :scope "provided"]
                 ;;[org.apache.spark/spark-streaming_2.12 "3.2.1" :scope "provided"]
                 [org.apache.spark/spark-mllib_2.12 "3.2.1" :scope "provided"]
                 ;;[com.github.fommil.netlib/all "1.1.2" :extension "pom"]
                 [org.apache.arrow/arrow-memory-netty "2.0.0" :scope "provided"]
                 [org.apache.arrow/arrow-memory-core "2.0.0" :scope "provided"]
                 [org.apache.arrow/arrow-vector "2.0.0" :scope "provided"
                  :exclusions [commons-codec com.fasterxml.jackson.core/jackson-databind]]
                 [com.fasterxml.jackson.core/jackson-databind "2.12.3" :scope "provided"]
                 [com.fasterxml.jackson.core/jackson-core "2.12.3" :scope "provided"]
                 [zero.one/fxl "0.0.6" :scope "provided"]
                 ]
  :aot :all
  :main clojure-spark-demo.core
  :repl-options {:init-ns clojure-spark-demo.core})
