from __future__ import annotations

from typing import Optional, List

from google.protobuf import empty_pb2
from google.protobuf.json_format import MessageToJson

from tq42.project import Project
from tq42.utils.exception_handling import handle_generic_sdk_errors

from com.terraquantum.organization.v2.organization.organization_pb2 import (
    OrganizationProto,
)
from com.terraquantum.organization.v2.organization.list_organizations_pb2 import (
    ListOrganizationsResponse,
)
from com.terraquantum.organization.v2.organization.get_organization_pb2 import (
    GetOrganizationRequest,
)

from typing import TYPE_CHECKING
from tq42.utils.pretty_list import PrettyList

# only import the stuff for type hints -> avoid circular imports
if TYPE_CHECKING:
    from tq42.client import TQ42Client


class Organization:
    """
    Reference an existing organization.

    :param client: a client instance
    :param id: the id of the existing organization
    :param data: only used internally
    """

    _client: TQ42Client
    id: str
    """ID of the organization"""
    data: OrganizationProto
    """Object containing all attributes of the organization"""

    def __init__(
        self, client: TQ42Client, id: str, data: Optional[OrganizationProto] = None
    ) -> None:
        self._client = client
        self.id = id

        if data:
            self.data = data
        else:
            self.data = self._get()

    def __repr__(self) -> str:
        return f"<Organization Id={self.id} Name={self.data.name}>"

    def __str__(self) -> str:
        return f"Organization: {MessageToJson(self.data, preserving_proto_field_name=True)}"

    @handle_generic_sdk_errors
    def _get(self) -> OrganizationProto:
        """
        Gets the information about the provided organization
        """
        get_org_request = GetOrganizationRequest(organization_id=self.id)
        res: OrganizationProto = self._client.organization_client.GetOrganization(
            request=get_org_request, metadata=self._client.metadata
        )
        return res

    @staticmethod
    def from_proto(client: TQ42Client, msg: OrganizationProto) -> Organization:
        """
        Creates organization instance from a protobuf message.

        :meta private:
        """
        return Organization(client=client, id=msg.id, data=msg)

    @handle_generic_sdk_errors
    def set(self) -> Organization:
        """
        Sets the current organization as the default organization.

        :returns: organization instance
        """
        project = Project.get_default(client=self._client, organization_id=self.id)
        if project:
            project.set()
            return self

        raise KeyError()

    @staticmethod
    @handle_generic_sdk_errors
    def get_default_org(client: TQ42Client) -> Optional[Organization]:
        """
        Gets the default organization for this user based on the default_org field

        :returns: the default organization if one is set as a default
        """
        org_list = list_all(client=client)
        if len(org_list) == 0:
            return None

        orgs_sorted = sorted(org_list, key=lambda o: o.id)
        return orgs_sorted[0]


@handle_generic_sdk_errors
def list_all(client: TQ42Client) -> List[Organization]:
    """
    List all the organizations you have permission to view.

    :param client: a client instance
    :returns: a list of all organizations
    """
    empty = empty_pb2.Empty()
    res: ListOrganizationsResponse = client.organization_client.ListOrganizations(
        request=empty, metadata=client.metadata
    )
    return PrettyList(
        [Organization.from_proto(client=client, msg=msg) for msg in res.organizations]
    )
