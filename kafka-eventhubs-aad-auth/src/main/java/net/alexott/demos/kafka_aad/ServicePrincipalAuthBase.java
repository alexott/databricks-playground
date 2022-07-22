package net.alexott.demos.kafka_aad;

import com.microsoft.aad.msal4j.ClientCredentialParameters;
import com.microsoft.aad.msal4j.ConfidentialClientApplication;
import com.microsoft.aad.msal4j.IAuthenticationResult;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.security.auth.AuthenticateCallbackHandler;
import org.apache.kafka.common.security.oauthbearer.OAuthBearerToken;
import org.apache.kafka.common.security.oauthbearer.OAuthBearerTokenCallback;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.security.auth.callback.Callback;
import javax.security.auth.callback.UnsupportedCallbackException;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Collections;
import java.util.Map;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeoutException;

/**
 * Base class for Service Principal based authentication
 */
abstract public class ServicePrincipalAuthBase implements AuthenticateCallbackHandler {
    protected volatile ConfidentialClientApplication msalClient;
    protected ClientCredentialParameters msalParameters;
    protected String authEndpoint;
    protected String clientId;

    private static final String AAD_TENANT_ID_KEY = "aad_tenant_id";
    private static final String AAD_AUTHORITY_ENDPOINT_KEY = "aad_authority_endpoint";
    private static final String AAD_CLIENT_ID_KEY = "aad_client_id";
    private static final Logger logger = LoggerFactory.getLogger(ServicePrincipalAuthBase.class);

    /**
     * Creates an instance of the client that will be used to obtain AAD tokens
     *
     * @return client that will be used to obtain AAD tokens
     * @throws MalformedURLException when authEndpoint URL is malformed
     */
    abstract ConfidentialClientApplication getClient() throws MalformedURLException;

    /**
     * Extracts common configuration properties, such as, AAD Tenant ID
     *
     * @param configs Kafka configuration parameters
     */
    protected void configureCommon(Map<String, ?> configs) {
        this.msalParameters = getMsalParameters(configs);

        String tenantId = configs.get(AAD_TENANT_ID_KEY).toString();
        clientId = configs.get(AAD_CLIENT_ID_KEY).toString();
        Object ob = configs.get(AAD_AUTHORITY_ENDPOINT_KEY);
        if (ob == null) {
            authEndpoint = "https://login.microsoftonline.com/";
        } else {
            authEndpoint = ob.toString();
        }
        authEndpoint += tenantId;
    }

    /**
     * Creates an instance of the parameters for MSAL. Currently only consists of the scope
     *
     * @param configs Kafka configs map
     * @return MSAL properties
     */
    static ClientCredentialParameters getMsalParameters(Map<String, ?> configs) {
        String bootstrapServer = configs.get(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG).toString();
        bootstrapServer = bootstrapServer.substring(1, bootstrapServer.length() - 2);
        bootstrapServer = bootstrapServer.substring(0, bootstrapServer.indexOf(':'));
        try {
            URL url = new URL("https", bootstrapServer, "/.default");
            return ClientCredentialParameters.builder(Collections.singleton(url.toString())).build();
        } catch (MalformedURLException e) {
            logger.info("Exception building scope: ", e);
        }
        return null;
    }

    @Override
    public void close() {
    }

    @Override
    public void handle(Callback[] callbacks) throws IOException, UnsupportedCallbackException {
        for (Callback callback : callbacks) {
            if (callback instanceof OAuthBearerTokenCallback) {
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
                    IAuthenticationResult authResult = this.msalClient.acquireToken(this.msalParameters).get();
                    // logger.debug("Token acquired: {}", authResult.accessToken());
                    OAuthBearerToken token = new KafkaOAuthBearerTokenImp(authResult.accessToken(), authResult.expiresOnDate());
                    OAuthBearerTokenCallback oauthCallback = (OAuthBearerTokenCallback) callback;
                    oauthCallback.token(token);
                } catch (InterruptedException | ExecutionException e) {
                    e.printStackTrace();
                }
            } else {
                throw new UnsupportedCallbackException(callback);
            }
        }
    }
}
