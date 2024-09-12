import unittest
from dataclasses import dataclass
from typing import cast

from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)
from com.terraquantum.experiment.v3alpha2.experimentrun.experiment_run_pb2 import (
    ExperimentRunProto,
    ExperimentRunResultProto,
)
from google.protobuf import struct_pb2

from tq42.cli.utils import formatter
from tq42.client import TQ42Client
from tq42.experiment_run import ExperimentRun, HardwareProto


class MockWithID:
    def __init__(self, id):
        self.id = id


@dataclass
class NameData:
    name: str


class MockWithNameResourceClasses(MockWithID):
    def __init__(self, id, name=None):
        super().__init__(id)
        self.data = NameData(name)


class MockWithName(MockWithID):
    def __init__(self, id, name=None):
        super().__init__(id)
        self.name = name


class MockList:
    def __init__(self, a):
        self.a = a


class MockOrgList(MockList):
    @property
    def organizations(self):
        return self.a


class MockProjList(MockList):
    @property
    def projects(self):
        return self.a


class MockExpList(MockList):
    @property
    def experiments(self):
        return self.a


class TestOutputFormat(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_format_org(self):
        org = MockWithID("ORG_ID")
        self.assertEqual('org="ORG_ID"', formatter.org_formatter.format(org))

    def test_format_org_by_project(self):
        proj = MockWithNameResourceClasses("PROJ_ID", name="Cool project")
        proj.data.organization_id = "ORG_ID"
        self.assertEqual(
            'org="ORG_ID"', formatter.org_formatter.format_by_project(proj)
        )

    def test_set_proj_lines(self):
        proj = MockWithNameResourceClasses("PROJ_ID", name="Cool project")
        proj.data.organization_id = "ORG_ID"
        expected = ['org="ORG_ID"', 'proj="Cool project" (PROJ_ID)']
        actual = formatter.set_proj_lines(proj)
        self.assertEqual(expected, actual)

    def test_format_org_list(self):
        a = [MockWithID("ORG_ID{}".format(i)) for i in range(2)]
        expected = ['org="ORG_ID0"', 'org="ORG_ID1"']
        actual = formatter.org_formatter.format_by_list_object(a)
        self.assertEqual(expected, actual)

    def test_format_proj(self):
        no_name_proj = MockWithNameResourceClasses("PROJ_ID0")
        proj = MockWithNameResourceClasses("PROJ_ID1", name="Cool Project!")
        self.assertEqual(
            'proj="PROJ_ID0"', formatter.proj_formatter.format(no_name_proj)
        )
        self.assertEqual(
            'proj="Cool Project!" (PROJ_ID1)', formatter.proj_formatter.format(proj)
        )

    def test_format_proj_list(self):
        a = [MockWithNameResourceClasses("PROJ_ID{}".format(i)) for i in range(2)]
        a[1].data.name = "Cool Project!"
        expected = ['proj="PROJ_ID0"', 'proj="Cool Project!" (PROJ_ID1)']
        actual = formatter.proj_formatter.format_by_list_object(a)
        self.assertEqual(expected, actual)

    def test_format_exp(self):
        no_name_exp = MockWithNameResourceClasses("EXP_ID0")
        exp = MockWithNameResourceClasses("EXP_ID1", name="Cool Experiment!")
        self.assertEqual('exp="EXP_ID0"', formatter.exp_formatter.format(no_name_exp))
        self.assertEqual(
            'exp="Cool Experiment!" (EXP_ID1)', formatter.exp_formatter.format(exp)
        )

    def test_format_exp_list(self):
        a = [MockWithNameResourceClasses("EXP_ID{}".format(i)) for i in range(2)]
        a[1].data.name = "Cool Experiment!"
        expected = ['exp="EXP_ID0"', 'exp="Cool Experiment!" (EXP_ID1)']
        actual = formatter.exp_formatter.format_by_list_object(a)
        self.assertEqual(expected, actual)

    def test_format_exp_run(self):
        exp_run = MockWithID("RUN_ID")
        self.assertEqual('run="RUN_ID"', formatter.run_formatter.format(exp_run))

    def test_format_exp_run_list(self):
        a = [MockWithID("RUN_ID{}".format(i)) for i in range(2)]
        expected = ['run="RUN_ID0"', 'run="RUN_ID1"']
        actual = formatter.run_formatter.format_by_list_object(a)
        self.assertEqual(expected, actual)

    def test_exp_run_created_lines(self):
        exp_run = MockWithID("RUN_ID")
        exp_run.status = 1
        expected = ['run="RUN_ID"', 'status="QUEUED"']
        actual = formatter.run_formatter.run_created_lines(exp_run)
        self.assertEqual(expected, actual)

    def test_exp_run_checked_lines(self):
        exp_run_data = MockWithID("RUN_ID")
        exp_run_data.status = 1
        exp_run_data.algorithm = "TOY"
        exp_run_data.hardware = 6
        exp_run_data.error_message = ""
        exp_run = ExperimentRun(client=None, id="RUN_ID", data=exp_run_data)

        expected = [
            'run="RUN_ID"',
            'status="QUEUED"',
            'algorithm="TOY"',
            'compute="LARGE_GPU"',
        ]
        actual = formatter.run_formatter.run_checked_lines(exp_run)
        self.assertEqual(expected, actual)

    def test_exp_run_checked_lines_completed(self):
        outcome = struct_pb2.Struct()
        outcome.update(
            {"result": {"y": 123}, "outputs": {"data": {"storage_id": "some-id"}}}
        )

        data = ExperimentRunProto(
            id="RUN_ID",
            experiment_id="exp_id",
            algorithm="TOY",
            status=ExperimentRunStatusProto.COMPLETED,
            hardware=HardwareProto.LARGE,
            result=ExperimentRunResultProto(outcome=outcome),
        )
        exp_run = ExperimentRun(client=cast(TQ42Client, None), id="RUN_ID", data=data)

        expected = [
            'run="RUN_ID"',
            'status="COMPLETED"',
            'algorithm="TOY"',
            'compute="LARGE"',
            'result="{"y": 123.0}"',
            'outputs="{"data": {"storage_id": "some-id"}}"',
        ]
        actual = formatter.run_formatter.run_checked_lines(exp_run)
        self.assertEqual(expected, actual)

    def test_exp_run_checked_lines_failed(self):
        data = ExperimentRunProto(
            id="RUN_ID",
            experiment_id="exp_id",
            algorithm="TOY",
            status=ExperimentRunStatusProto.FAILED,
            hardware=HardwareProto.LARGE,
            error_message="error message",
        )
        exp_run = ExperimentRun(client=cast(TQ42Client, None), id="RUN_ID", data=data)

        expected = [
            'run="RUN_ID"',
            'status="FAILED"',
            'algorithm="TOY"',
            'compute="LARGE"',
            'error_message="error message"',
        ]
        actual = formatter.run_formatter.run_checked_lines(exp_run)
        self.assertEqual(expected, actual)

    def test_exp_run_checked_lines_not_done(self):
        data = ExperimentRunProto(
            id="RUN_ID",
            experiment_id="exp_id",
            algorithm="TOY",
            status=ExperimentRunStatusProto.RUNNING,
            hardware=HardwareProto.LARGE,
        )
        exp_run = ExperimentRun(client=cast(TQ42Client, None), id="RUN_ID", data=data)

        expected = [
            'run="RUN_ID"',
            'status="RUNNING"',
            'algorithm="TOY"',
            'compute="LARGE"',
        ]
        actual = formatter.run_formatter.run_checked_lines(exp_run)
        self.assertEqual(expected, actual)
