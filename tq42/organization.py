from __future__ import annotations

from typing import Optional, List

from google.protobuf import empty_pb2
from google.protobuf.json_format import MessageToJson

from tq42.project import Project
from tq42.exception_handling import handle_generic_sdk_errors

from com.terraquantum.organization.v1.organization.organization_pb2 import (
    OrganizationProto,
    ListOrganizationsResponse,
)
from com.terraquantum.organization.v1.organization.get_organization_request_pb2 import (
    GetOrganizationRequest,
)

from typing import TYPE_CHECKING

from tq42.utils.pretty_list import PrettyList

# only import the stuff for type hints -> avoid circular imports
if TYPE_CHECKING:
    from tq42.client import TQ42Client


class Organization:
    """
    Class to manage organization
    """

    client: TQ42Client
    id: str
    data: OrganizationProto

    def __init__(
        self, client: TQ42Client, id: str, data: Optional[OrganizationProto] = None
    ) -> None:
        self.client = client
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
        get_org_request = GetOrganizationRequest(id=self.id)
        res: OrganizationProto = self.client.organization_client.GetOrganization(
            request=get_org_request, metadata=self.client.metadata
        )
        return res

    @staticmethod
    def from_proto(client: TQ42Client, msg: OrganizationProto) -> Organization:
        """
        Creates organization instance from a protobuf message.
        """
        return Organization(client=client, id=msg.id, data=msg)

    @handle_generic_sdk_errors
    def set(self) -> Organization:
        """
        Sets the given organization as the default.
        """
        project = Project.get_default(client=self.client, organization_id=self.id)
        if project:
            project.set()
            return self

        raise KeyError()

    @staticmethod
    @handle_generic_sdk_errors
    def get_default_org(client: TQ42Client) -> Optional[Organization]:
        """
        Gets the default organization for this user based on the default_org field
        """
        org_list = list_all(client=client)
        for org in org_list:
            if org.data.default_org and org.data.default_org is True:
                return org
        return None


@handle_generic_sdk_errors
def list_all(client: TQ42Client) -> List[Organization]:
    """
    List all the organizations you have permission to view.

    For details, see
    https://docs.tq42.com/en/latest/Python_Developer_Guide/Setting_Up_Your_Environment.html#list-all-organizations
    """
    empty = empty_pb2.Empty()
    res: ListOrganizationsResponse = (
        client.organization_client.ListAssignedOrganizations(
            request=empty, metadata=client.metadata
        )
    )
    return PrettyList(
        [Organization.from_proto(client=client, msg=msg) for msg in res.organizations]
    )
