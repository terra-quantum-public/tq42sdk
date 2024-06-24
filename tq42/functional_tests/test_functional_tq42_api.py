import unittest
import uuid

from tq42.compute import list_all as list_all_computes
from tq42.organization import list_all as list_all_organizations, Organization
from tq42.project import Project, list_all as list_all_projects
from tq42.experiment import Experiment, list_all as list_all_experiments
from tq42.experiment_run import ExperimentRun, list_all as list_all_experiment_runs
from tq42.functional_tests.functional_test_config import FunctionalTestConfig
from tq42.algorithm import (
    ToyMetadataProto,
    ToyParametersProto,
    ToyInputsProto,
    AlgorithmProto,
)
from tq42.compute import HardwareProto
from google.protobuf.json_format import MessageToDict

from com.terraquantum.experiment.v1.experimentrun.experiment_run_pb2 import (
    ExperimentRunStatusProto,
)


class TestFunctionalTQ42API(unittest.TestCase, FunctionalTestConfig):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_org_list(self):
        org_list_obj = list_all_organizations(client=self.get_client())

        # Expect that there is at least one project in project list
        self.assertGreater(len(org_list_obj), 0)

        # Expect that specific project is in project list
        org_ids = [org.id for org in org_list_obj]
        self.assertIn(self.org, org_ids)

    def test_org_get(self):
        org = Organization(client=self.get_client(), id=self.org)
        self.assertEqual(self.org, org.id)
        # TODO: We need the appropriate enum for status
        self.assertEqual(1, org.data.state)
        self.assertTrue(org.data.default_org)

    def test_compute_show(self):
        # TODO: Currently compute show does nothing real. Improve test once fully implemented.

        compute = list_all_computes()
        self.assertIsNotNone(compute)

    def test_proj_list(self):
        proj_list = list_all_projects(
            client=self.get_client(), organization_id=self.org
        )

        # Expect that there is at least one project in project list
        self.assertGreater(len(proj_list), 0)

        # Expect that specific project is in project list
        proj_ids = [proj.id for proj in proj_list]
        self.assertIn(self.proj, proj_ids)

    def test_proj_get(self):
        proj = Project(client=self.get_client(), id=self.proj)

        self.assertEqual(self.proj, proj.id)
        self.assertEqual(self.org, proj.data.organization_id)

    def test_exp_list(self):
        exp_list = list_all_experiments(client=self.get_client(), project_id=self.proj)

        # Expect that there is at least one experiment in experiment list
        self.assertGreater(len(exp_list), 0)

        # Expect that specific experiment is in experiment list
        exp_ids = [exp.id for exp in exp_list]
        self.assertIn(self.exp, exp_ids)

    def test_exp_get(self):
        exp = Experiment(client=self.get_client(), id=self.exp)

        self.assertEqual(self.exp, exp.id)
        self.assertEqual(self.proj, exp.data.project_id)

    def test_exp_run_list(self):
        exp_runs = list_all_experiment_runs(
            client=self.get_client(), experiment_id=self.exp
        )

        # Expect that there is at least one experiment run for this experiment
        self.assertGreater(len(exp_runs), 0)

        # Expect that specific experiment run is in experiment list
        exp_run_ids = [exp_run.id for exp_run in exp_runs]
        self.assertIn(self.exp_run, exp_run_ids)

    def test_exp_run_get(self):
        exp_run = ExperimentRun(client=self.get_client(), id=self.exp_run)

        self.assertEqual(self.exp_run, exp_run.id)
        self.assertEqual(self.exp, exp_run.data.experiment_id)

    def test_exp_run_create(self):
        parameters = ToyMetadataProto(
            parameters=ToyParametersProto(n=2, r=1, msg="correct"),
            inputs=ToyInputsProto(),
        )
        parameters = MessageToDict(parameters, preserving_proto_field_name=True)
        exp_run = ExperimentRun.create(
            client=self.get_client(),
            algorithm=AlgorithmProto.TOY,
            experiment_id=self.exp,
            compute=HardwareProto.SMALL,
            parameters=parameters,
        )
        self.assertEqual(self.exp, exp_run.data.experiment_id)
        self.assertEqual(ExperimentRunStatusProto.QUEUED, exp_run.data.status)

    def test_exp_set_friendly_name(self):
        random_string = str(uuid.uuid4())
        updated_exp = Experiment(client=self.get_client(), id=self.exp).update(
            name=random_string
        )
        self.assertEqual(updated_exp.data.name, random_string)

    def test_proj_set_friendly_name(self):
        random_string = str(uuid.uuid4())
        updated_project = Project(client=self.get_client(), id=self.proj).update(
            name=random_string
        )
        self.assertEqual(updated_project.data.name, random_string)
