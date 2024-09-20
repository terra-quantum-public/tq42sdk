from __future__ import annotations

from google.protobuf import empty_pb2

from com.terraquantum.plan.v1.plan.check_functionality_request_pb2 import (
    CheckFunctionalityRequest,
    FunctionalityProto,
)

from typing import TYPE_CHECKING

# only import the stuff for type hints -> avoid circular imports
if TYPE_CHECKING:
    from tq42.client import TQ42Client


class Functionality:
    """
    Reference a functionality.
    """

    @staticmethod
    def check(
        client: TQ42Client, organization_id: str, functionality_type: str, version: str
    ) -> None:
        """
        Checks if a functionality with given version should be accessible for the given organization.
        """
        req = CheckFunctionalityRequest(
            organization_id=organization_id,
            functionality=FunctionalityProto(type=functionality_type, version=version),
        )
        res: empty_pb2.Empty = client.plan_client.CheckFunctionality(
            request=req, metadata=client.metadata
        )
        return res
