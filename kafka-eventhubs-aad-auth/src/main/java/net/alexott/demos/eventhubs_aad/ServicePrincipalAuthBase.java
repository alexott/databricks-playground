package net.alexott.demos.eventhubs_aad;

import com.microsoft.aad.msal4j.ClientCredentialParameters;
import com.microsoft.aad.msal4j.ConfidentialClientApplication;
import com.microsoft.aad.msal4j.IAuthenticationResult;
import org.apache.kafka.common.protocol.types.Field;
import org.apache.spark.eventhubs.utils.AadAuthenticationCallback;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.Collections;

import scala.collection.immutable.Map;
import java.util.concurrent.CompletableFuture;
import scala.collection.JavaConverters;

abstract class ServicePrincipalAuthBase implements AadAuthenticationCallback {
    protected volatile ConfidentialClientApplication msalClient;
    protected final String authority; // tenant ID
    protected String authEndpoint;
    protected final String clientId;

    private static final String AAD_TENANT_ID_KEY = "aad_tenant_id";
    private static final String AAD_AUTHORITY_ENDPOINT_KEY = "aad_authority_endpoint";
    private static final String AAD_CLIENT_ID_KEY = "aad_client_id";
    private static final Logger logger = LoggerFactory.getLogger(ServicePrincipalAuthBase.class);

    ServicePrincipalAuthBase(Map<String, String> params) {
        java.util.Map<String, String> m = JavaConverters.mapAsJavaMapConverter(params).asJava();
//        String mapStr = m.entrySet().stream()
//            .map(e -> "'" + e.getKey() + "'='" + e.getValue() + "'")
//            .collect(Collectors.joining(", "));
//        logger.info("params: {}", mapStr);
        this.authority = m.get(AAD_TENANT_ID_KEY);
        this.clientId = m.get(AAD_CLIENT_ID_KEY);
        this.authEndpoint = m.getOrDefault(AAD_AUTHORITY_ENDPOINT_KEY, "https://login.microsoftonline.com/");
        if (!this.authEndpoint.endsWith("/")) {
            this.authEndpoint += "/";
        }
        this.authEndpoint += this.authority;
    }

    /**
     * Creates an instance of the client that will be used to obtain AAD tokens
     *
     * @return client that will be used to obtain AAD tokens
     * @throws MalformedURLException when authEndpoint URL is malformed
     */
    abstract ConfidentialClientApplication getClient() throws MalformedURLException;

    @Override
    public String authority() {
        return authority;
    }

    @Override
    public CompletableFuture<String> acquireToken(String audience, String authority,  Object state) {
        try {
            if (this.msalClient == null) {
                synchronized (this) {
                    if (this.msalClient == null) {
                        this.msalClient = getClient();
                        if (this.msalClient == null) {
                            throw new IOException("Can't create MSAL client");
                        }
                    }
                }
            }
            ClientCredentialParameters ccParams = ClientCredentialParameters.builder(
                Collections.singleton(audience + ".default")).build();
            return this.msalClient.acquireToken(ccParams).thenApply(IAuthenticationResult::accessToken);
        } catch (IOException ex) {
            CompletableFuture<String> failed = new CompletableFuture<>();
            failed.completeExceptionally(ex);
            return failed;
        }
    }
}
