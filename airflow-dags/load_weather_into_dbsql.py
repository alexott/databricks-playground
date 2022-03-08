import json
from typing import Optional
from datetime import date

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.databricks.operators.databricks_sql import (
    DatabricksCopyIntoOperator,
    DatabricksSqlOperator,
)
from airflow.providers.microsoft.azure.transfers.local_to_wasb import LocalFilesystemToWasbOperator
from airflow.utils.dates import days_ago

# constants to change
WASBS_CONN_ID = 'wasbs-test'
DATABRICKS_SQL_ENDPOINT_NAME = "Airflow Test"
DATABRICKS_CONN_ID = "my-shard-pat"
DESTINATION_TABLE_NAME = "default.airflow_weather"
LANDING_LOCATION_PREFIX = "airflow/landing"
ADLS_CONTAINER_NAME = "test"
ADLS_STORAGE_NAME = "test"

#
cities = ["london", "berlin", "amsterdam"]
BASE_API_URL = "https://weatherdbi.herokuapp.com/data/weather/"
ADLS_LANDING_LOCATION = f"abfss://{ADLS_CONTAINER_NAME}@{ADLS_STORAGE_NAME}.dfs.core.windows.net/" \
                        f"{LANDING_LOCATION_PREFIX}/ "


airflow_default_args = {
    "owner": "airflow",
    "databricks_conn_id": DATABRICKS_CONN_ID,
    "sql_endpoint_name": DATABRICKS_SQL_ENDPOINT_NAME,
}


def import_city_data(city: str):
    def convert_percents_string(s: str) -> Optional[float]:
        if s and s.endswith('%'):
            return float(s[:-1]) / 100
        return None

    url = BASE_API_URL + city.lower()
    req = requests.get(url)
    data_json = req.json()
    data = {'date': str(date.today()),
            'region': data_json['region'],
            'temperature': data_json['currentConditions']['temp']['c'],
            'precipitation': convert_percents_string(data_json['currentConditions']['precip']),
            'humidity': convert_percents_string(data_json['currentConditions']['humidity']),
            'wind': data_json['currentConditions']['wind']['km'],
            'condition': data_json['currentConditions']['comment'],
            'next_days': [{'day': d['day'], 'condition': d['comment'],
                           'max_temp': d['max_temp']['c'], 'min_temp': d['min_temp']['c']}
                          for d in data_json.get('next_days', [])],
            }
    return data


def get_weather_data(output_path: str):
    data = [json.dumps(import_city_data(city)) + "\n" for city in cities]
    with open(output_path, "w") as f:
        f.writelines(data)


with DAG(
        "load_weather_into_dbsql",
        start_date=days_ago(0),
        schedule_interval="@daily",
        default_args=airflow_default_args,
        catchup=False,
) as dag:
    schema = "date date, condition STRING, humidity double, precipitation double, region STRING, " \
             "temperature long, wind long, next_days ARRAY<STRUCT<condition: STRING, day: STRING, " \
             "max_temp: long, min_temp: long>>"

    create_table = DatabricksSqlOperator(
        task_id="create_table",
        sql=[f"create table if not exists {DESTINATION_TABLE_NAME}({schema}) using delta"],
    )

    get_weather_data = PythonOperator(task_id="get_weather_data",
                                      python_callable=get_weather_data,
                                      op_kwargs={
                                          "output_path": "/tmp/{{next_ds}}.json"
                                      },
                                      )

    copy_data_to_adls = LocalFilesystemToWasbOperator(
        task_id='upload_weather_data',
        wasb_conn_id=WASBS_CONN_ID,
        file_path="/tmp/{{next_ds}}.json",
        container_name='test',
        blob_name= LANDING_LOCATION_PREFIX + "/{{next_ds}}.json",
        load_options={"overwrite": True,},
    )

    import_weather_data = DatabricksCopyIntoOperator(
        task_id="import_weather_data",
        expression_list="date::date, * except(date)",
        table_name=DESTINATION_TABLE_NAME,
        file_format="JSON",
        file_location=ADLS_LANDING_LOCATION,
        files=["{{next_ds}}.json"],
        #validate=True, # this requires Preview channel
        force_copy=True,
    )

    (create_table >> get_weather_data >> copy_data_to_adls >> import_weather_data)
