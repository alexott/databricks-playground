from databricks import sql
from databricks.sdk.core import azure_service_principal, Config
import os

def get_env_or_raise(name: str) -> str:
  value = os.environ[name]
  if not value:
    raise Exception(f"Environment variable {name} isn't set or empty")

  return value

# Variables to fill
# Host name without https://
host_name="adb-xxx.17.azuredatabricks.net"
# Path obtained as per instructions https://docs.databricks.com/dev-tools/python-sql-connector.html#get-started
http_path="/sql/1.0/warehouses/xxx"
# Your query to execute
query = "select * from samples.nyctaxi.trips limit 5"


# Explicit initialization of the authenticator
tenant_id = get_env_or_raise("ARM_TENANT_ID")
client_id = get_env_or_raise("ARM_CLIENT_ID")
client_secret = get_env_or_raise("ARM_CLIENT_SECRET")

creds = azure_service_principal(Config(azure_client_secret=client_secret, azure_client_id=client_id,
                                       azure_tenant_id=tenant_id, host=f"https://{host_name}"))

# Implicit initialization - you need to specify corresponding environment variables
# creds = azure_service_principal(Config())

with sql.connect(server_hostname=host_name, http_path=http_path,
                 credentials_provider=lambda: creds) as connection:
  cursor = connection.cursor()
  cursor.execute(query)
  result = cursor.fetchall()

  for row in result:
    print(row)

  cursor.close()
  connection.close()
