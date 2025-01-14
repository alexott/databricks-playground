package net.alexott.demos;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;

class OssJDBCOAuthAzureServicePrincipal {

    public static void main(String[] args) throws Exception {
        // Variables to set
        String query = "select 42, current_timestamp(), current_catalog(), current_database(), current_user()";
        String clientId = "...";
        String clientSecret = "...";
        String host = "adb-....azuredatabricks.net";
        String httpPath = "/sql/1.0/warehouses/...";
        String jdbcString = String.format("jdbc:databricks://%s:443/default;transportMode=http;ssl=1;httpPath=%s;AuthMech=11;Auth_Flow=1;OAuth2ClientId=%s;OAuth2Secret=%s",
                host, httpPath, clientId, clientSecret);

        String JDBC_DRIVER = "com.databricks.client.jdbc.Driver";

        Class.forName(JDBC_DRIVER);
        System.out.println("Getting JDBC connection");
        try (Connection conn = DriverManager.getConnection(jdbcString);
            Statement stmt = conn.createStatement()) {
            System.out.println("Going to execute query");
            try (ResultSet rs = stmt.executeQuery(query)) {
                System.out.println("Query is executed");
                ResultSetMetaData md = rs.getMetaData();
                String[] columns = new String[md.getColumnCount()];
                for (int i = 0; i < columns.length; i++) {
                    columns[i] = md.getColumnName(i + 1);
                }
                while (rs.next()) {
                    System.out.print("Row " + rs.getRow() + "=[");
                    for (int i = 0; i < columns.length; i++) {
                        if (i != 0) {
                            System.out.print(", ");
                        }
                        System.out.print(columns[i] + "='" + rs.getObject(i + 1) + "'");
                    }
                    System.out.println(")]");
                }
            }
        }
        System.exit(0);
    }
}
