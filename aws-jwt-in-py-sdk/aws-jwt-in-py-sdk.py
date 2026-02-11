import os

from databricks.sdk import WorkspaceClient
from databricks.sdk import oidc
from databricks.sdk.core import (Config, CredentialsProvider, credentials_strategy, oidc_credentials_provider)

import boto3


audience = "my-demo-audience"
duration = 300
signing_algorithm = "RS256"
tags = [
    {'Key': 'team', 'Value': 'data-engineering'},
    {'Key': 'environment', 'Value': 'production'}
]


# TODO: think how to pass these parameters to the constructor
class AwsJwtIdTokenSource(oidc.IdTokenSource):
    def __init__(self, audience: str):
        self.audience = audience
        self.duration = duration
        self.signing_algorithm = signing_algorithm
        self.tags = tags
        s3_client = boto3.client('s3')
        self.region = s3_client.meta.region_name

    def id_token(self) -> oidc.IdToken:
        sts_client = boto3.client('sts', region_name=self.region)
        response = sts_client.get_web_identity_token(
            Audience=[self.audience],
            DurationSeconds=self.duration,
            SigningAlgorithm=self.signing_algorithm,
            Tags=self.tags
        )
        token = response['WebIdentityToken']
        return oidc.IdToken(jwt=token)


@credentials_strategy("aws-jwt", ["token_audience"])
def aws_jwt_strategy(cfg: Config) -> CredentialsProvider:
    return oidc_credentials_provider(cfg, AwsJwtIdTokenSource(audience=cfg.token_audience))


host = os.getenv( "DATABRICKS_HOST") or "https://adb-.....17.azuredatabricks.net"
client_id=os.getenv("CLIENT_ID") or "..."

cfg=Config(host=host, 
           client_id=client_id, 
           credentials_strategy=aws_jwt_strategy, 
           token_audience=audience)
wc = WorkspaceClient(config=cfg)

for cluster in wc.clusters.list():
    print(cluster.cluster_id, cluster.cluster_name)