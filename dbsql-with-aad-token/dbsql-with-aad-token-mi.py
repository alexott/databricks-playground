from typing import Dict, Optional

from databricks import sql
import requests
import time
import os

from databricks.sql.auth.authenticators import AuthProvider

# Variables to fill
# Host name without https://
host_name = "adb-.....17.azuredatabricks.net"
# Path obtained as per instructions https://docs.databricks.com/dev-tools/python-sql-connector.html#get-started
http_path = "/sql/1.0/warehouses/951d1b041fc6c792"
# Your query to execute
query = "select 42, current_timestamp(), current_catalog(), current_database(), current_user()"

TOKEN_REFRESH_LEAD_TIME = 120
DEFAULT_DATABRICKS_SCOPE = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d"
AZURE_MANAGEMENT_ENDPOINT = "https://management.core.windows.net/"
AZURE_METADATA_SERVICE_TOKEN_URL = "http://169.254.169.254/metadata/identity/oauth2/token"


# Heavily based on the Apache Airflow implementation that is originally written by me
# https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/how-to-use-vm-token
class AzureMIAuthProvider(AuthProvider):
    def __init__(self, uami_application_id: Optional[str] = None,
                 databricks_resource_id: Optional[str] = None):
        """

        :param uami_application_id: optional client ID of User Assigned Managed Identity
        :param databricks_resource_id: optional Azure Databricks resource ID
        """
        self.__uami_application_id = uami_application_id
        self.__databricks_resource_id = databricks_resource_id
        self.__oauth_tokens = {}

    @staticmethod
    def _is_oauth_token_valid(token: dict, time_key="expires_on") -> bool:
        if "access_token" not in token or token.get("token_type",
                                                    "") != "Bearer" or time_key not in token:
            raise Exception(f"Can't get necessary data from OAuth token: {token}")
        return int(token[time_key]) > (int(time.time()) + TOKEN_REFRESH_LEAD_TIME)

    def _get_aad_token(self, resource: str) -> str:
        aad_token = self.__oauth_tokens.get(resource)
        if aad_token and self._is_oauth_token_valid(aad_token):
            return aad_token["access_token"]
        params = {
            "api-version": "2018-02-01",
            "resource": resource,
        }
        if self.__uami_application_id:
            params["client_id"] = self.__uami_application_id
        resp = requests.get(AZURE_METADATA_SERVICE_TOKEN_URL, params=params,
                            headers={"Metadata": "true"}, timeout=2,
                            )
        resp.raise_for_status()
        jsn = resp.json()

        self._is_oauth_token_valid(jsn)
        self.__oauth_tokens[resource] = jsn
        return jsn["access_token"]

    def __call__(self, *args, **kwargs):
        request_headers = {}
        if self.__databricks_resource_id:
            mgmt_token = self._get_aad_token(AZURE_MANAGEMENT_ENDPOINT)
            request_headers["X-Databricks-Azure-Workspace-Resource-Id"] = self.__databricks_resource_id
            request_headers["X-Databricks-Azure-SP-Management-Token"] = mgmt_token

        request_headers["Authorization"] = f"Bearer {self._get_aad_token(DEFAULT_DATABRICKS_SCOPE)}"
        # print(request_headers)
        return request_headers


creds = AzureMIAuthProvider(uami_application_id=os.getenv("ARM_CLIENT_ID"),
                            databricks_resource_id=os.getenv("DATABRICKS_AZURE_RESOURCE_ID"))

with sql.connect(server_hostname=host_name, http_path=http_path,
                 credentials_provider=lambda: creds) as connection:
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        print(row)

    cursor.close()
    connection.close()
