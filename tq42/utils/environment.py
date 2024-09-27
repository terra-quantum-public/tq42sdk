from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from tq42.organization import Organization, list_all as list_all_organizations
from tq42.project import Project, list_all as list_all_projects
from tq42.utils import dirs, file_handling
from tq42.utils.cache import clear_cache

from typing import TYPE_CHECKING

# only import the stuff for type hints -> avoid circular imports
if TYPE_CHECKING:
    from tq42.client import TQ42Client

_DEFAULT_BASE_URL = "terraquantum.io"
_DEFAULT_CLIENT_ID = "gvBa4BHKOTlotDuE6E2HSQBzBDlM00F4"
_DEFAULT_SCOPE = "openid profile email offline_access tq42"


@dataclass
class ConfigEnvironment:
    """
    Configuration environment for the TQ42 SDK
    """

    base_url: str
    client_id: str
    scope: str

    @property
    def api_host(self):
        return "api.{}".format(self.base_url)

    @property
    def channels_host(self):
        return f"channels.{self.base_url}"

    @property
    def auth_url_token(self):
        return f"https://auth.{self.base_url}/oauth/token"

    @property
    def auth_url_code(self):
        return f"https://auth.{self.base_url}/oauth/device/code"

    @property
    def audience(self):
        return f"https://graphql-gateway.{self.base_url}/graphql"

    @property
    def client_credential_flow_audience(self):
        return f"https://api.{self.base_url}"

    @property
    def headers(self):
        return {"Content-Type": "application/x-www-form-urlencoded"}

    @property
    def code_data(self):
        return {
            "client_id": self.client_id,
            "scope": self.scope,
            "audience": self.audience,
        }

    def token_data(self, device_code: str):
        return {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code,
            "client_id": self.client_id,
        }

    def refresh_token_data(self, refresh_token: str):
        return {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
        }

    def client_credentials_data(
        self, client_id: str, client_secret: str, audience: str
    ):
        return {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "audience": audience,
        }

    @staticmethod
    def from_env() -> "ConfigEnvironment":
        base_url = os.getenv("TQ42_BASE_URL", _DEFAULT_BASE_URL)
        client_id = os.getenv("TQ42_CLIENT_ID", _DEFAULT_CLIENT_ID)
        scope = os.getenv("TQ42_SCOPE", _DEFAULT_SCOPE)

        return ConfigEnvironment(base_url=base_url, client_id=client_id, scope=scope)


def get_environment() -> str:
    content = file_handling.read_file(dirs.cache_file())
    return content


def environment_clear() -> str:
    clear_cache()
    return get_environment()


def environment_default_set(
    client: TQ42Client, organization: Optional[Organization] = None
) -> str:
    if organization is None:
        organization = Organization.get_default_org(client=client)

    organization.set()

    content = file_handling.read_file(dirs.cache_file())
    return content


def get_default_org(client: TQ42Client) -> Optional[Organization]:
    org_list = list_all_organizations(client=client)
    for org in org_list:
        if org.data.default_org and org.data.default_org is True:
            return org
    return None


def get_default_proj(client: TQ42Client, org_id: str) -> Optional[Project]:
    # get default proj id
    project_list = list_all_projects(client=client, organization_id=org_id)

    for proj in project_list:
        if proj.data.default_project and proj.data.default_project is True:
            return proj

    return None
