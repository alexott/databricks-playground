from databricks import sql
from azure.identity import ClientSecretCredential
import os

def get_env_or_raise(name: str) -> str:
  value = os.environ[name]
  if not value:
    raise Exception(f"Environment variable {name} isn't set or empty")

  return value

tenant_id = get_env_or_raise("ARM_TENANT_ID")
client_id = get_env_or_raise("ARM_CLIENT_ID")
client_secret = get_env_or_raise("ARM_CLIENT_SECRET")
csc = ClientSecretCredential(tenant_id, client_id, client_secret)

dbx_scope = '2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default'
aad_token = csc.get_token(dbx_scope).token

# Variables to fill
# Host name without https://
host_name=""
# Path obtained as per instructions https://docs.databricks.com/dev-tools/python-sql-connector.html#get-started
http_path=""
# Your query to execute
query = ""

connection = sql.connect(
  server_hostname=host_name,
  http_path=http_path,
  access_token=aad_token)

cursor = connection.cursor()

cursor.execute(query)

result = cursor.fetchall()

for row in result:
  print(row)

cursor.close()
