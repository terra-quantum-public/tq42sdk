import unittest
from dataclasses import dataclass

from tq42.cli.output_format import formatter


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
        exp_run = MockWithID("RUN_ID")
        exp_run.status = 1
        exp_run.algorithm = 6
        exp_run.hardware = 5
        exp_run.result = "ERROR"
        exp_run.error_message = ""

        expected = [
            'run="RUN_ID"',
            'status="QUEUED"',
            'algorithm="TOY"',
            'compute="MEDIUM_GPU"',
            'result="ERROR"',
            #'' signifies no error message expected as status is QUEUED
            # if error expected, this field should show:
            # error_message="Example error message."
            "",
        ]
        actual = formatter.run_formatter.run_checked_lines(exp_run)
        self.assertEqual(expected, actual)
