from __future__ import annotations
from typing import Optional

from tq42.organization import Organization, list_all as list_all_organizations
from tq42.project import Project, list_all as list_all_projects
from tq42.utils import dirs, file_handling
from tq42.utils.cache import clear_cache

from typing import TYPE_CHECKING

# only import the stuff for type hints -> avoid circular imports
if TYPE_CHECKING:
    from tq42.client import TQ42Client


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
