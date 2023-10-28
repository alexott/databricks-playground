# Azure Active Directory authentication for Spark Kafka & EventHubs connectors accessing Event Hubs

This directory contains a library for using Azure Active Directory tokens to connect to the Azure Event Hubs using the Spark Kafka connector via Kafka protocol or [Spark EventHubs connector](https://github.com/Azure/azure-event-hubs-spark/).

## Using Spark Kafka connector on Databricks Runtime version 12.2+ and Delta Live Tables

Since DBR 12.2, the Apache Kafka client that is used by Databricks Runtime is upgraded to versions that are directly supporting OAuth/OIDC flows, so there is no need to build this library - you just need to correctly configure Kafka consumer, like this:

```py
topic = "<topic>"
eh_namespace_name = "<eh_namespace_name>"
eh_server = f"{eh_namespace_name}.servicebus.windows.net"

# Data for service principal are stored in the secret scope
tenant_id = dbutils.secrets.get("scope", "tenant_id")
client_id = dbutils.secrets.get("scope", "sp-id")
client_secret = dbutils.secrets.get("scope", "sp-secret")
# Generate
sasl_config = f'kafkashaded.org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required clientId="{client_id}" clientSecret="{client_secret}" scope="https://{eh_server}/.default" ssl.protocol="SSL";'

# Create Kafka options dictionary
callback_class = "kafkashaded.org.apache.kafka.common.security.oauthbearer.secured.OAuthBearerLoginCallbackHandler"
kafka_options = {
  "kafka.bootstrap.servers": f"{eh_server}:9093",
  "subscribe": topic,
  "startingOffsets": "earliest",
  "kafka.security.protocol": "SASL_SSL",
  "kafka.sasl.mechanism": "OAUTHBEARER",
  "kafka.sasl.jaas.config": sasl_config,
  "kafka.sasl.oauthbearer.token.endpoint.url": f"https://login.microsoft.com/{tenant_id}/oauth2/v2.0/token",
  "kafka.sasl.login.callback.handler.class": callback_class,
}

df = spark.readStream.format("kafka").options(**kafka_options).load()
```


## Build the library for DBR runtime versions below 12.2

You need to select profile to build this project:

| Profile name | Supported DBR versions       | Status     |
|--------------|------------------------------|------------|
|`dbr-10.4`    | DBR 10.4, DBR 11.3, DBR 12.2 | tested     |
|`dbr-9.1`     | DBR 9.1 LTS                  | not tested |
|`dbr-7.3`     | DBR 7.3 LTS                  | not tested |


and then use it to build package using Maven:

```sh
mvn clean package -P profile-name
```

that will generate a jar file with name `kafka-eventhubs-aad-auth-<version>-<dbr_version>.jar` in the `target` directory. Add this library to a Databricks cluster or Databricks job.  You also need to add `com.microsoft.azure:msal4j:1.10.1` library to a cluster/job, as it isn't shipped together with Databricks runtimes.  If you use this library to access via EventHubs protocol, you need to add corresponding library using following coordinates: `com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.22`.

## Configure Service Principal

Right now this library supports following authentication methods:

1. using Service Principal client ID & secret
1. (coming soon) using Service Principal certificate

Service principal should have following permissions on the specific topic:

* `Azure Event Hubs Data Receiver` - for consuming from Event Hubs
* `Azure Event Hubs Data Sender` - for writing to Event Hubs

## Use with Spark Kafka connector

All authentication methods should provide following options:

* `kafka.aad_tenant_id` - required Azure Active Directory Tenant ID
* `kafka.aad_client_id` - Service Principal Client ID (also called "Application ID", **don't use Object ID!**).
* `kafka.aad_authority_endpoint` - optional host name of Azure AD authentication endpoint if you're using special [Azure Cloud (GovCloud, China, Germany)](https://docs.microsoft.com/en-us/graph/deployments#app-registration-and-token-service-root-endpoints). The value must contain a protocol and end with `/`. For example: `https://login.microsoftonline.de/`.  Default value is `https://login.microsoftonline.com/`.
* `kafka.security.protocol` should be set to `SASL_SSL`
* `kafka.sasl.mechanism` should be set to `OAUTHBEARER`
* `kafka.sasl.jaas.config` should be set to `kafkashaded.org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required;` (trailing `;` is required!)


### Authenticating using Service Principal client ID & secret

We need to provide following options:

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

## Use with EventHubs

All authentication methods should provide following options:

* `aad_tenant_id` - required Azure Active Directory Tenant ID
* `aad_client_id` - Service Principal Client ID (also called "Application ID", **don't use Object ID!**).
* `aad_authority_endpoint` - optional host name of Azure AD authentication endpoint if you're using special [Azure Cloud (GovCloud, China, Germany)](https://docs.microsoft.com/en-us/graph/deployments#app-registration-and-token-service-root-endpoints). The value must contain a protocol and end with `/`. For example: `https://login.microsoftonline.de/`.  Default value is `https://login.microsoftonline.com/`.
* `eventhubs.useAadAuth` - should be set to `True`
* `eventhubs.AadAuthCallbackParams` - is the JSON-encoded dictionary with parameters that will be passed to callback handler's class constructor.
* `eventhubs.aadAuthCallback` - is the class name of specific implementation

### Authenticating using Service Principal client ID & secret

We need to provide additional options:

* `aad_client_secret` - Service Principal Client Secret (it's recommended to store it in the Azure KeyVault-baked secret scope and retrieve it via `dbutils.secrets.get`).
* `eventhubs.aadAuthCallback` should be set to the name of the class: `net.alexott.demos.eventhubs_aad.ServicePrincipalCredentialsAuth`

This authentication method needs following parameters in the parameters dictionary:

* `aad_tenant_id` (described above)
* `aad_client_id` (described above)
* `aad_client_secret` - Service Principal Client Secret (it's recommended to store it in the Azure KeyVault-baked secret scope and retrieve it via `dbutils.secrets.get`).

Example:

```python
topic = "..."
tenant_id = "..."
client_id = "..."
client_secret = dbutils.secrets.get("secret_scope", "sp-secret")
ehs_ns_name = "eventhubs-namespace-name"
callback_class_name = "net.alexott.demos.eventhubs_aad.ServicePrincipalCredentialsAuth"
# Instead of `servicebus.windows.net` there could be regional endpoints
ehs_endpoint = f"sb://{ehs_ns_name}.servicebus.windows.net"

# EventHubs connection string.
connectionString = f"Endpoint=sb://{ehs_ns_name}.servicebus.windows.net;EntityPath={topic}"

# Parameters that will be passed to the callback function
params = {
  "aad_tenant_id": tenant_id,
  "aad_client_id": client_id,
  "aad_client_secret": client_secret,
}

# Spark EventHubs options
ehConf = {
  'eventhubs.connectionString': sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connectionString),
  'eventhubs.useAadAuth': True,
  'eventhubs.aadAuthCallback': callback_class_name,
  'eventhubs.AadAuthCallbackParams': json.dumps(params),
}

df = spark.readStream.format("eventhubs").options(**ehConf).load()
```


## Limitations

* We currently support only one bootstrap server for Kafka


## Troubleshooting

### TopicAuthorizationException: Not authorized to access topics

Check that service principal has correct permission for all Event Hubs topics as described above

### No OAuth Bearer tokens in Subject's private credentials

Usually is caused the incorrect configuration, check Spark logs to see actual exception.


## Project Support

Please note that this project is provided for your exploration only, and are not formally supported by Databricks with Service Level Agreements (SLAs).  They are provided AS-IS and we do not make any guarantees of any kind.  Please do not submit a support ticket relating to any issues arising from the use of this project.

Any issues discovered through the use of this project should be filed as GitHub Issues on the Repo.  They will be reviewed as time permits, but there are no formal SLAs for support.
