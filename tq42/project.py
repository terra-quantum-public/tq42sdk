from __future__ import annotations

from typing import Optional, List

from google.protobuf.field_mask_pb2 import FieldMask
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToJson

from tq42.exception_handling import handle_generic_sdk_errors
from tq42.utils.pretty_list import PrettyList
from tq42.utils.utils_for_cache import (
    get_current_value,
    write_key_value_to_cache,
    clear_cache,
)

from com.terraquantum.project.v1.project.project_pb2 import ProjectProto
from com.terraquantum.project.v1.project.get_project_request_pb2 import (
    GetProjectRequest,
)
from com.terraquantum.project.v1.project.update_project_request_pb2 import (
    UpdateProjectRequest,
)
from com.terraquantum.project.v1.project.list_projects_request_pb2 import (
    ListProjectsRequest,
)
from com.terraquantum.project.v1.project.list_projects_response_pb2 import (
    ListProjectsResponse,
)

from typing import TYPE_CHECKING

# only import the stuff for type hints -> avoid circular imports
if TYPE_CHECKING:
    from tq42.client import TQ42Client


class Project:
    """
    Class to manage projects
    """

    client: TQ42Client
    id: str
    data: ProjectProto

    def __init__(
        self, client: TQ42Client, id: str, data: Optional[ProjectProto] = None
    ) -> None:
        self.client = client
        self.id = id

        if data:
            self.data = data
        else:
            self.data = self._get()

    def __repr__(self) -> str:
        return f"<Project Id={self.id} Name={self.data.name}>"

    def __str__(self) -> str:
        return f"Project: {MessageToJson(self.data, preserving_proto_field_name=True)}"

    @handle_generic_sdk_errors
    def _get(self) -> ProjectProto:
        """
        Gets the data corresponding to this project id.
        """
        get_proj_request = GetProjectRequest(id=self.id)
        res = self.client.project_client.GetProject(
            request=get_proj_request, metadata=self.client.metadata
        )
        return res

    @staticmethod
    def from_proto(client: TQ42Client, msg: ProjectProto) -> Project:
        """
        Creates Project instance from a protobuf message.
        """
        return Project(client=client, id=msg.id, data=msg)

    @handle_generic_sdk_errors
    def update(self, name: str) -> Project:
        """
        Updates this specific project
        """
        project = {
            "id": self.id,
            "name": name,
        }

        # Create a new FieldMask instance
        field_mask = FieldMask()

        # Add paths to the FieldMask
        field_mask.paths.append("id")
        field_mask.paths.append("name")

        update_proj_request = UpdateProjectRequest(
            project=project,
            update_mask=field_mask,
            request_id=None,
        )
        self.data = self.client.project_client.UpdateProject(
            request=update_proj_request, metadata=self.client.metadata
        )
        return self

    @handle_generic_sdk_errors
    def set_friendly_name(self, friendly_name: str) -> Project:
        """
        Set a friendly name for a project.

        For details, see
        https://docs.tq42.com/en/latest/Python_Developer_Guide/Setting_Up_Your_Environment.html#setting-friendly-names-for-projects-and-experiments
        """
        return self.update(name=friendly_name)

    @staticmethod
    @handle_generic_sdk_errors
    def show(client: TQ42Client) -> Project:
        """
        Returns the current default project.
        If no default proj can be found return NoDefaultError
        """
        proj = get_current_value("proj")
        return Project(client=client, id=proj)

    @handle_generic_sdk_errors
    def set(self) -> Project:
        """
        If projectId is valid for the given user sets this projectId
        and the corresponding organizationId as the default
        """
        clear_cache()
        write_key_value_to_cache("org", self.data.organization_id)
        write_key_value_to_cache("proj", self.id)

        return self

    @staticmethod
    @handle_generic_sdk_errors
    def get_default(client: TQ42Client, organization_id: str) -> Optional[Project]:
        """
        Gets the default project for this user and organization_id based on the default_project field
        """
        project_list = list_all(client=client, organization_id=organization_id)
        if len(project_list) == 0:
            return None

        for proj in project_list:
            if proj.data.default_project and proj.data.default_project is True:
                return proj

        def access_created_at(project: Project) -> Timestamp:
            return project.data.created_at

        projects_sorted = sorted(project_list, key=access_created_at)
        return projects_sorted[0]


@handle_generic_sdk_errors
def list_all(
    client: TQ42Client, organization_id: Optional[str] = None
) -> List[Project]:
    """
    List all the projects you have permission to view within the organization that is currently set.

    For details, see
    https://docs.tq42.com/en/latest/Python_Developer_Guide/Setting_Up_Your_Environment.html#list-all-projects
    """

    if not organization_id:
        organization_id = get_current_value("org")

    create_list_proj_request = ListProjectsRequest(organization_id=organization_id)

    res: ListProjectsResponse = client.project_client.ListProjects(
        request=create_list_proj_request, metadata=client.metadata
    )
    return PrettyList(
        [Project.from_proto(client=client, msg=data) for data in res.projects]
    )
