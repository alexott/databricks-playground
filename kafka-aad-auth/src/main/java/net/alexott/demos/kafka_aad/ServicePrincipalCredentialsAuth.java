package net.alexott.demos.kafka_aad;

import com.microsoft.aad.msal4j.ClientCredentialFactory;
import com.microsoft.aad.msal4j.ConfidentialClientApplication;
import com.microsoft.aad.msal4j.IClientCredential;

import javax.security.auth.login.AppConfigurationEntry;
import java.net.MalformedURLException;
import java.util.List;
import java.util.Map;

public class ServicePrincipalCredentialsAuth extends ServicePrincipalAuthBase {
    private String clientId;
    private String clientSecret;

    // private static final Logger logger = LoggerFactory.getLogger(ServicePrincipalCredentialsAuth.class);

    private static final String AAD_CLIENT_ID_KEY = "aad_client_id";
    private static final String AAD_CLIENT_SECRET_KEY = "aad_client_secret";

    @Override
    public void configure(Map<String, ?> configs, String mechanism,
                          List<AppConfigurationEntry> jaasConfigEntries) {
        configureCommon(configs);
        clientId = configs.get(AAD_CLIENT_ID_KEY).toString();
        clientSecret = configs.get(AAD_CLIENT_SECRET_KEY).toString();
    }

    @Override
    ConfidentialClientApplication getClient() throws MalformedURLException {
        IClientCredential credential = ClientCredentialFactory.createFromSecret(this.clientSecret);
        return ConfidentialClientApplication.builder(this.clientId, credential)
            .authority(this.authEndpoint)
            .build();
    }
}
