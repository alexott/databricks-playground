from typing import Dict
import os

from azure.identity import ManagedIdentityCredential
from databricks.sdk import WorkspaceClient
from databricks.sdk.config import Config
from databricks.sdk.credentials_provider import CredentialsProvider, \
    CredentialsStrategy


class AzureIdentityCredentialsStrategy(CredentialsStrategy):
    def auth_type(self) -> str:
        return 'azure-mi'

    def __init__(self, client_id: str = None):
        self.client_id = client_id

    def __call__(self, cfg: 'Config') -> CredentialsProvider:
        if self.client_id:
            mi_credential = ManagedIdentityCredential(client_id=self.client_id)
        else:
            mi_credential = ManagedIdentityCredential()

        def inner() -> Dict[str, str]:
            token = mi_credential.get_token("2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default")
            return {'Authorization': f'Bearer {token.token}'}

        return inner


client_id = os.getenv( "AZURE_CLIENT_ID")
host = os.getenv( "DATABRICKS_HOST") or "https://adb-....17.azuredatabricks.net"

wc = WorkspaceClient(host=host,
                     credentials_strategy=AzureIdentityCredentialsStrategy(client_id=client_id))

for cluster in wc.clusters.list():
    print(cluster.cluster_id, cluster.cluster_name)