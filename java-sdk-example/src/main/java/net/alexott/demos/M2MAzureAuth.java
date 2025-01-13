package net.alexott.demos;

import com.databricks.sdk.WorkspaceClient;
import com.databricks.sdk.core.DatabricksConfig;
import com.databricks.sdk.service.compute.ClusterDetails;
import com.databricks.sdk.service.compute.ClusterSource;
import com.databricks.sdk.service.compute.ListClustersRequest;
import com.databricks.sdk.service.compute.ListClustersFilterBy;

import java.util.Arrays;

class M2MAzureAuth {
    public static void main(String[] args) {
        // implicit configuration - via environment variables
        // https://github.com/databricks/databricks-sdk-java?tab=readme-ov-file#azure-native-authentication
        WorkspaceClient client = null;
        if (System.getenv("IMPLICIT_AUTH") != null) {
            client = new WorkspaceClient();
        } else {
            DatabricksConfig config = new DatabricksConfig().setAuthType("azure-client-secret")
                    .setAzureClientId(System.getenv("DATABRICKS_CLIENT_ID"))
                    .setAzureClientSecret(System.getenv("DATABRICKS_CLIENT_SECRET"))
                    .setAzureTenantId(System.getenv("DATABRICKS_TENANT_ID"))
                    .setHost(System.getenv("DATABRICKS_HOST"));
            client = new WorkspaceClient(config);
        }
        System.out.println("Client: " + client.config());
        for (ClusterDetails c : client.clusters().list(new ListClustersRequest().setFilterBy(
                new ListClustersFilterBy().setClusterSources(Arrays.asList(ClusterSource.UI, ClusterSource.API))))) {
            System.out.println(c.getClusterName());
        }
    }
}