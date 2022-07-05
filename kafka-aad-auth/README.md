# Azure Active Directory authentication for Spark Kafka connector accessing Event Hubs

This directory contains a library for using Azure Active Directory tokens to connect to the Azure Event Hubs using the Spark Kafka connector via Kafka protocol.

# Build

You need to select profile to build this project:

| Profile name | Supported DBR versions  | Status     |
|--------------|--------------------------------------|
|`dbr-10.4`    | DBR 10.4+, DBR 11.x     | tested     |
|`dbr-9.1`     | DBR 9.1 LTS             | not tested |
|`dbr-7.3`     | DBR 7.3 LTS             | not tested |


and then use it to build package using Maven:

```sh
mvn clean package -P profile-name
```

that will generate a jar file with name `kafka-aad-auth-<version>-<dbr_version>.jar` in the `target` directory. Add this library to a Databricks cluster or Databricks job.  Please note that for 7.3 & 9.1 versions you will need to add `com.microsoft.azure:msal4j:1.10.1` library to a cluster/job, as it isn't shipped together with these Databricks runtimes

# Configure & use

Right now this library supports following authentication methods:

1. using Service Principal client ID & secret
1. (coming soon) using Service Principal certificate

Service principal should have following permissions on the specific topic:

* `Azure Event Hubs Data Receiver` - for consuming from Event Hubs
* `Azure Event Hubs Data Sender` - for writing to Event Hubs

All authentication methods should provide following options:

* `kafka.aad_tenant_id` - required Azure Active Directory Tenant ID
* `kafka.aad_authority_endpoint` - optional host name of Azure AD authentication endpoint if you're using special [Azure Cloud (GovCloud, China, Germany)](https://docs.microsoft.com/en-us/graph/deployments#app-registration-and-token-service-root-endpoints>. The value must contain a protocol and end with `/`. For example: `https://login.microsoftonline.de/`.  Default value is `https://login.microsoftonline.com/`.
* `kafka.security.protocol` should be set to `SASL_SSL`
* `kafka.sasl.mechanism` should be set to `OAUTHBEARER`
* `kafka.sasl.jaas.config` should be set to `kafkashaded.org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;` (trailing `;` is required!)


## Authenticating using Service Principal client ID & secret

We need to provide following options:

* `kafka.aad_tenant_id` - Service Principal Client ID (also called "Application ID", **don't use Object ID!**).
* `kafka.aad_client_secret` - Service Principal Client Secret (it's recommended to store it in the Azure KeyVault-baked secret scope and retrieve it via `dbutils.secrets.get`).
* `kafka.sasl.login.callback.handler.class` should be set to the name of the class: `net.alexott.demos.kafka_aad.ServicePrincipalCredentialsAuth`

Example:

```python
sasl_config = "kafkashaded.org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;"
topic = "..."
tenant_id = "..."
client_id = "..."
client_secret = dbutils.secrets.get("secret_scope", "sp-secret")

kafka_options = {
  "kafka.bootstrap.servers": "<eventhubs_namespace>.servicebus.windows.net:9093",
  "subscribe": topic,
  "failOnDataLoss": "false",
  "startingOffsets": "earliest",
  "kafka.security.protocol": "SASL_SSL",
  "kafka.sasl.mechanism": "OAUTHBEARER", 
  "kafka.sasl.jaas.config": sasl_config,
  "kafka.sasl.login.callback.handler.class": "net.alexott.demos.kafka_aad.ServicePrincipalCredentialsAuth",
  "kafka.aad_tenant_id": tenant_id,
  "kafka.aad_client_id": client_id,
  "kafka.aad_client_secret": client_secret,
}

df = (
    spark 
    .readStream
    .format("kafka") 
    .options(**kafka_options)
    .load()
  )
```

# Limitations

* We currently support only one bootstrap server


# Troubleshooting

## TopicAuthorizationException: Not authorized to access topics

Check that service principal has correct permission for all Event Hubs topics as described above

## No OAuth Bearer tokens in Subject's private credentials

Usually is caused the incorrect configuration, check Spark logs to see actual exception.
