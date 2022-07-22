package net.alexott.demos.eventhubs_aad;

import com.microsoft.aad.msal4j.ClientCredentialFactory;
import com.microsoft.aad.msal4j.ConfidentialClientApplication;
import com.microsoft.aad.msal4j.IClientCredential;


import java.net.MalformedURLException;
import scala.collection.immutable.Map;

public class ServicePrincipalCredentialsAuth extends ServicePrincipalAuthBase {
    private final String clientSecret;

    private static final String AAD_CLIENT_SECRET_KEY = "aad_client_secret";

    public ServicePrincipalCredentialsAuth(Map<String, String> params) {
        super(params);
        clientSecret = params.get(AAD_CLIENT_SECRET_KEY).get();
    }

    @Override
    ConfidentialClientApplication getClient() throws MalformedURLException {
        IClientCredential credential = ClientCredentialFactory.createFromSecret(this.clientSecret);
        return ConfidentialClientApplication.builder(this.clientId, credential)
            .authority(this.authEndpoint)
            .build();
    }

}
