package net.alexott.demos.kafka_aad;

import com.microsoft.aad.msal4j.ClientCredentialFactory;
import com.microsoft.aad.msal4j.ConfidentialClientApplication;
import com.microsoft.aad.msal4j.IClientCredential;

import javax.security.auth.login.AppConfigurationEntry;
import java.net.MalformedURLException;
import java.util.List;
import java.util.Map;

/**
 * Class for generation of AAD tokens based on the Service Principal Client ID & Secret
 */
public class ServicePrincipalCredentialsAuth extends ServicePrincipalAuthBase {
    private String clientSecret;

    private static final String AAD_CLIENT_SECRET_KEY = "aad_client_secret";

    @Override
    public void configure(Map<String, ?> configs, String mechanism, List<AppConfigurationEntry> jaasConfigEntries) {
        configureCommon(configs);
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
