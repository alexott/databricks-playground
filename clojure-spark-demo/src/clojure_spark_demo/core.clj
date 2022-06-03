(ns clojure-spark-demo.core
  (:require [zero-one.geni.core :as g])
  (:gen-class)
  )


(defn -main [& args]
  (let* [source (g/read-csv! "dbfs:/databricks-datasets/flights/departuredelays.csv"
                             {:header "true" :infer-schema "true"})]
    (println "Source schema")
    (g/print-schema source)
    (println "rows count: " (g/count source))
    (println "going to write data to a table")
    (-> source
        (g/select :date :delay :distance :origin :destination)
        (g/write-table! "default.clj_test" {:mode "overwrite"})
        )
    )
  )
