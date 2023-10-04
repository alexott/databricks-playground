from databricks import sql
import os


def get_env_or_raise(name: str) -> str:
    value = os.environ[name]
    if not value:
        raise Exception(f"Environment variable {name} isn't set or empty")

    return value


# Variables to fill
# Host name without https://
host_name = "adb-xxxx.17.azuredatabricks.net"
# Path obtained as per instructions https://docs.databricks.com/dev-tools/python-sql-connector.html#get-started
http_path = "/sql/1.0/warehouses/xxx"
# Your query to execute
query = "select * from samples.nyctaxi.trips limit 5"

# Explicit initialization of the authenticator
client_id = get_env_or_raise("ARM_CLIENT_ID")

with sql.connect(server_hostname=host_name, http_path=http_path,
                 auth_type="databricks-oauth",
                 oauth_client_id=client_id
                 ) as connection:
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        print(row)

    cursor.close()
    connection.close()
