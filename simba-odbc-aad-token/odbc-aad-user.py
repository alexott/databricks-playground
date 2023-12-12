import pyodbc

# Update parameters
host="adb-....17.azuredatabricks.net"
http_path = "/sql/1.0/warehouses/...."
driver = "/Library/simba/spark/lib/libsparkodbc_sb64-universal.dylib"
query = "select 42, current_timestamp(), current_catalog(), current_database(), current_user()"

#
url = f"Driver={driver};Host={host};Port=443;ThriftTransport=2;SSL=1;AuthMech=11;Auth_Flow=2;HTTPPath={http_path};IgnoreTransactions=true;PWD=1234567"
db_conn = pyodbc.connect(url)

cursor = db_conn.cursor().execute(query)
columns = [column[0] for column in cursor.description]
results = [dict(zip(columns, row)) for row in cursor]
print(results)
