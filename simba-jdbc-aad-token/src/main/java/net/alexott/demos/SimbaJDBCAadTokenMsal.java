package net.alexott.demos;

import com.microsoft.aad.msal4j.ClientCredentialFactory;
import com.microsoft.aad.msal4j.ClientCredentialParameters;
import com.microsoft.aad.msal4j.ConfidentialClientApplication;
import com.microsoft.aad.msal4j.IAuthenticationResult;
import com.microsoft.aad.msal4j.IClientCredential;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;
import java.util.Collections;
import java.util.Set;

class SimbaJDBCAadTokenMsal {

    public static void main(String[] args) throws Exception {
        // Variables to set
        String query = "";
        String tenantId = "";
        String clientId = "";
        String clientSecret = "";
        String jdbcString = "jdbc:databricks://<host>:443/default;transportMode=http;ssl=1;httpPath=<http_path>;AuthMech=11;Auth_Flow=0;Auth_AccessToken=";

        //
        String authority = "https://login.microsoftonline.com/" + tenantId;

        System.out.println("Going to acquire token");
        IClientCredential cred = ClientCredentialFactory.createFromSecret(clientSecret);
        ConfidentialClientApplication app = ConfidentialClientApplication.builder(clientId, cred ).authority(authority).build();

        Set<String> databricksScope = Collections.singleton("2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default");
        ClientCredentialParameters authParameters = ClientCredentialParameters.builder(databricksScope).build();
        IAuthenticationResult authResult = app.acquireToken(authParameters).join();

        String JDBC_DRIVER = "com.databricks.client.jdbc.Driver";
        String DB_URL = jdbcString + authResult.accessToken();

        Class.forName(JDBC_DRIVER);
        System.out.println("Getting JDBC connection");
        try (Connection conn = DriverManager.getConnection(DB_URL);
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
