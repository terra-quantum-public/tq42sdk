import os.path
import time
import unittest

from tq42.dataset import Dataset, list_all as list_all_datasets, DatasetSensitivityProto
from tq42.functional_tests.functional_test_config import FunctionalTestConfig

from com.terraquantum.storage.v1alpha1.storage_pb2 import StorageStatusProto


class TestFunctionalTQ42APIDataset(unittest.TestCase, FunctionalTestConfig):
    dataset_id: str
    dataset_name = "Dataset Name Test1"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_proj_dataset_create(self):
        dataset = Dataset.create(
            client=self.get_client(),
            project_id=self.proj,
            name=self.dataset_name,
            description="Dataset description test 1",
            url="gs://circuit-runner-demo",
            sensitivity=DatasetSensitivityProto.CONFIDENTIAL,
        )
        TestFunctionalTQ42APIDataset.dataset_id = dataset.id
        self.assertEqual("Dataset Name Test1", dataset.data.name)

        # make sure dataset is properly available
        time.sleep(3)

        # waiting for the dataset transfer to be completed
        while dataset.data.status not in [
            StorageStatusProto.FAILED,
            StorageStatusProto.COMPLETED,
            StorageStatusProto.EMPTY,
        ]:
            dataset._refresh()
            time.sleep(3)

        self.assertEqual(StorageStatusProto.COMPLETED, dataset.data.status)

    def test_proj_dataset_get(self):
        dataset = Dataset(
            client=self.get_client(), id=TestFunctionalTQ42APIDataset.dataset_id
        )
        self.assertEqual(self.dataset_name, dataset.data.name)

    def test_proj_datasets_list(self):
        datasets = list_all_datasets(client=self.get_client(), project_id=self.proj)
        found_id = any(
            TestFunctionalTQ42APIDataset.dataset_id in dataset.id
            for dataset in datasets
        )
        self.assertTrue(found_id)

    def test_proj_dataset_export(self):
        dataset_export = Dataset(
            client=self.get_client(), id=TestFunctionalTQ42APIDataset.dataset_id
        ).export(".")

        assert 1 == len(dataset_export)
        assert os.path.exists(dataset_export[0])

        try:
            os.remove(dataset_export[0])
        except OSError:
            pass

        assert not os.path.exists(dataset_export[0])
