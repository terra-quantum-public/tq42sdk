import unittest
from unittest.mock import MagicMock, patch
from google.protobuf.json_format import ParseDict
from grpc import StatusCode
from grpc._channel import _InactiveRpcError as InactiveRpcError, _RPCState as RPCState

from com.terraquantum.project.v2 import project_pb2 as proj_def
from com.terraquantum.project.v2 import list_projects_pb2
from com.terraquantum.organization.v2.organization import organization_pb2 as org_def

from tq42.client import TQ42Client
from tq42.organization import Organization
from tq42.project import Project
from tq42.exceptions import NoDefaultError, InvalidArgumentError


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TQ42Client()

    def tearDown(self):
        pass

    def test_client_structure(self):
        self.assertTrue(hasattr(TQ42Client, "login"))
        self.assertTrue(hasattr(TQ42Client, "__enter__"))
        self.assertTrue(hasattr(TQ42Client, "__exit__"))

    def test_context_manager_behavior(self):
        with TQ42Client() as client:
            # Assert that the __enter__ method is called
            self.assertEqual(client.__enter__(), client)

            # Perform some operations inside the context
            client.metadata

            self.assertNotEqual(client.__exit__(None, None, None), client)

        # Assert that the __exit__ method is called after exiting the context
        self.assertEqual(client.__exit__(None, None, None), None)

    @patch("tq42.project.get_current_value")
    def test_proj_show_no_proj_set(self, get_current_value_mock):
        get_current_value_mock.side_effect = KeyError("key error")
        self.assertRaises(NoDefaultError, Project.show, self.client)

    @patch("tq42.project.get_current_value")
    def test_proj_show_default_proj_set(self, get_current_value_mock):
        project = {
            "id": "this-is-random-but-valid-uuid",
            "organization_id": "this-is-a-random-org-id-1",
            "name": "right project",
            "description": "this is the right project",
        }
        project = ParseDict(project, proj_def.ProjectProto())
        self.assertIsNotNone(project)
        self.client.project_client.GetProject = MagicMock(return_value=project)
        get_current_value_mock.return_value = "this-is-a-random-but-valid-uuid"
        res = Project.show(client=self.client)
        self.assertIsNotNone(res)
        self.assertEqual(1, self.client.project_client.GetProject.call_count)
        self.assertEqual(
            "this-is-a-random-but-valid-uuid",
            self.client.project_client.GetProject.call_args[1]["request"].project_id,
        )
        self.assertEqual("right project", res.data.name)

    @patch("tq42.project.write_key_value_to_cache")
    @patch("tq42.project.clear_cache")
    def test_proj_set(self, clear_cache_mock, write_key_value_to_cache_mock):
        project = {
            "id": "new-project-uuid-we-wanna-set",
            "organization_id": "this-is-a-random-org-id-1",
            "name": "right project",
            "description": "this is the right project",
        }

        cache = {}

        def add_stuff_to_dict(key: str, value: str) -> None:
            cache[key] = value

        write_key_value_to_cache_mock.side_effect = add_stuff_to_dict

        project = ParseDict(project, proj_def.ProjectProto())
        self.client.project_client.GetProject = MagicMock(return_value=project)
        Project(client=self.client, id="new-project-uuid-we-wanna-set").set()

        self.assertEqual(1, clear_cache_mock.call_count)
        self.assertEqual(2, write_key_value_to_cache_mock.call_count)
        self.assertDictEqual(
            cache,
            {
                "proj": "new-project-uuid-we-wanna-set",
                "org": "this-is-a-random-org-id-1",
            },
        )

    def test_project_not_found(self):
        get_project_mock = MagicMock()
        get_project_mock.side_effect = InactiveRpcError(
            RPCState(
                code=StatusCode.INVALID_ARGUMENT,
                details="no details",
                due=[],
                initial_metadata=[],
                trailing_metadata=[],
            )
        )

        self.client.project_client.GetProject = get_project_mock
        self.assertRaises(
            InvalidArgumentError,
            Project,
            client=self.client,
            id="this-project-id-is-impossible-to-find",
        )

    @patch("tq42.project.write_key_value_to_cache")
    @patch("tq42.project.clear_cache")
    def test_org_set(self, clear_cache_mock, write_key_value_to_cache_mock):
        org = {
            "id": "new-org-uuid-we-wanna-set",
            "name": "just-so-random-org",
            "description": "random description for org",
        }

        projects_dict = {
            "projects": [
                {
                    "id": "nfec987b-bf43-46e5-a0f0-85bc08c9cf18",
                    "organization_id": "new-org-uuid-we-wanna-set",
                    "name": "Ymixer shape optimization",
                },
                {
                    "id": "new-proj-uuid-we-wanna-set",
                    "organization_id": "new-org-uuid-we-wanna-set",
                    "name": "b225f5e5-eaa0-47d0-8ef0-7e954da6d681",
                },
            ]
        }

        projects = ParseDict(projects_dict, list_projects_pb2.ListProjectsResponse())
        self.assertIsNotNone(projects)

        cache = {}

        def add_stuff_to_dict(key: str, value: str) -> None:
            cache[key] = value

        write_key_value_to_cache_mock.side_effect = add_stuff_to_dict

        org = ParseDict(org, org_def.OrganizationProto())
        self.client.organization_client.GetOrganization = MagicMock(return_value=org)

        self.client.project_client.ListProjects = MagicMock(return_value=projects)

        Organization(client=self.client, id="new-org-uuid-we-wanna-set").set()

        self.assertEqual(1, clear_cache_mock.call_count)
        self.assertEqual(2, write_key_value_to_cache_mock.call_count)
        expected = {
            "org": "new-org-uuid-we-wanna-set",
            "proj": "new-proj-uuid-we-wanna-set",
        }
        self.assertDictEqual(cache, expected)

    def test_org_not_found(self):
        get_org_mock = MagicMock()
        get_org_mock.side_effect = InactiveRpcError(
            RPCState(
                code=StatusCode.INVALID_ARGUMENT,
                details="no details",
                due=[],
                initial_metadata=[],
                trailing_metadata=[],
            )
        )

        self.client.organization_client.GetOrganization = get_org_mock

        self.assertRaises(
            InvalidArgumentError,
            Organization,
            client=self.client,
            id="this-org-id-is-impossible-to-find",
        )
