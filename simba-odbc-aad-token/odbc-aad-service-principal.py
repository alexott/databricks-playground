import pyodbc
import os


def get_env_or_raise(name: str) -> str:
    value = os.environ[name]
    if not value:
        raise Exception(f"Environment variable {name} isn't set or empty")

    return value


# Update parameters
host="adb-....17.azuredatabricks.net"
http_path = "/sql/1.0/warehouses/..."
driver = "/Library/simba/spark/lib/libsparkodbc_sb64-universal.dylib"
client_id = get_env_or_raise("ARM_CLIENT_ID")
client_secret = get_env_or_raise("ARM_CLIENT_SECRET")

#
url = f"Driver={driver};Host={host};Port=443;ThriftTransport=2;SSL=1;AuthMech=11;Auth_Flow=1;HTTPPath={http_path};IgnoreTransactions=true;Auth_Client_ID={client_id};Auth_Client_Secret={client_secret}"
db_conn = pyodbc.connect(url)

query = "select 42, current_timestamp(), current_catalog(), current_database(), current_user()"
cursor = db_conn.cursor().execute(query)
columns = [column[0] for column in cursor.description]
results = [dict(zip(columns, row)) for row in cursor]
print(results)
